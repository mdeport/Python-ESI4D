from django.shortcuts import render, redirect
from django.db import transaction
from django.utils import timezone
from datetime import timedelta

from .forms.forms_new_return import LoanReturnForm

from .models import Loan
from .forms.forms_new import LoanNewForm

# Create your views here.


def index_loans(request):
    loans = Loan.objects.select_related("book").all()
    return render(request, "loans/index.html", {"loans": loans})

def new_loan(request):
    if request.method == "POST":
        form = LoanNewForm(request.POST)
        if form.is_valid():
            loan = form.save(commit=False)

            if not loan.date_loan:
                loan.date_loan = timezone.now()

            # définir la date limite à +14 jours
            loan.date_limit_return = loan.date_loan + timedelta(days=14)

            # définir l'état
            loan.state_book_returned = "loan"

            book = loan.book
            # vérifier disponibilité
            if book.number_of_books_available <= 0:
                form.add_error("book", "Aucun exemplaire disponible pour ce livre.")
            else:
                # transaction pour décrémenter et sauver le prêt
                with transaction.atomic():
                    book = type(book).objects.select_for_update().get(pk=book.pk)
                    if book.number_of_books_available <= 0:
                        form.add_error("book", "Aucun exemplaire disponible pour ce livre.")
                    else:
                        book.number_of_books_available -= 1
                        book.save()
                        loan.save()
                        return redirect("index_loans")
    else:
        form = LoanNewForm()

    return render(request, "loans/new.html", {"form": form})

def return_loan(request):
    if request.method == "POST":
        form = LoanReturnForm(request.POST)
        if form.is_valid():
            loan_selected = form.cleaned_data["loan"]
            date_ret = form.cleaned_data["date_returned"]
            comments = form.cleaned_data.get("comments", "")

            with transaction.atomic():
                loan = Loan.objects.select_for_update().select_related("book").get(pk=loan_selected.pk)
                if loan.date_returned is not None:
                    form.add_error("loan", "Cet emprunt a déjà été retourné.")
                else:
                    # chiffrage du retour
                    loan.date_returned = date_ret
                    loan.state_book_returned = "returned"
                    if comments:
                        loan.comments = (loan.comments or "") + "\n" + comments
                    loan.save()

                    # incrémenter number_of_books_available
                    book = loan.book.__class__.objects.select_for_update().get(pk=loan.book.pk)
                    new_available = book.number_of_books_available + 1
                    if book.number_of_book_possessed is not None:
                        book.number_of_books_available = min(new_available, book.number_of_book_possessed)
                    else:
                        book.number_of_books_available = new_available
                    book.save()

                    return redirect("index_loans")
    else:
        form = LoanReturnForm()

    return render(request, "loans/new_return.html", {"form": form})