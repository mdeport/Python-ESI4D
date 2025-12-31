from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from .forms.forms_new import BookForm
from .models import Book

# Create your views here.
def index_book(request: HttpResponse) -> HttpResponse:
    books = Book.objects.all()
    return render(request, "books/index.html", {"books": books})

def new_book(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("index_book") 
    else:
        form = BookForm()
    return render(request, "books/new.html", {"form": form})



def show_book(request: HttpResponse, book_id: int) -> HttpResponse:
    book = get_object_or_404(Book,id=book_id)
    return render(request, "books/show.html", {"book": book})

def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect("show_book", book_id=book.id)
    else:
        form = BookForm(instance=book)
    return render(request, "books/edit.html", {"form": form, "book": book})