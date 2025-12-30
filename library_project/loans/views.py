from django.shortcuts import render, redirect
from django.db import transaction
from django.utils import timezone
from datetime import timedelta

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

            # définir la date de prêt si non fournie
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
                    # verrou basique : recharger l'objet pour éviter condition de concurrence
                    book = type(book).objects.select_for_update().get(pk=book.pk)
                    if book.number_of_books_available <= 0:
                        form.add_error("book", "Aucun exemplaire disponible pour ce livre.")
                    else:
                        book.number_of_books_available -= 1
                        book.save()
                        loan.save()
                        return redirect("loans_index")  # adapte le nom si besoin
    else:
        form = LoanNewForm()

    return render(request, "loans/new.html", {"form": form})