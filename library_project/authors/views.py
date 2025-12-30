from datetime import datetime
from django.shortcuts import redirect, render, get_object_or_404
from .forms.forms_new import AuthorForm
from .models import Author

# Create your views here.
def index_author(request):
    authors = Author.objects.all()
    return render(request, "authors/index.html", {"authors": authors})

def new_author(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("index_author")
    else:
        form = AuthorForm()
    return render(request, "authors/new.html", {"form": form})

def show_author(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    return render(request, "authors/show.html", {"author": author})