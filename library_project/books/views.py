from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse

from authors.models import Author
from .models import Book

# Create your views here.
def index_book(request: HttpResponse) -> HttpResponse:
    books = Book.objects.all()
    return render(request, "books/index.html", {"books": books})

def new_book(request):
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        isbn = request.POST.get("isbn", "")
        published_date = request.POST.get("published_date", "")
        price = request.POST.get("price", "")
        author_id = request.POST.get("author")

        if title and author_id:
            Book.objects.create(title=title, isbn=isbn, published_date=published_date, price=price, author_id=author_id)
            return redirect("index_book")

    authors = Author.objects.all()
    return render(request, "books/new.html", {"authors": authors})



def show_book(request: HttpResponse, book_id: int) -> HttpResponse:
    book = get_object_or_404(Book,id=book_id)
    return render(request, "books/show.html", {"book": book})
