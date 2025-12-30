from django.shortcuts import redirect, render, get_object_or_404

from .models import Author

# Create your views here.
def index_author(request):
    authors = Author.objects.all()
    return render(request, "authors/index.html", {"authors": authors})

def new_author(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        birth_date = request.POST.get("birth_date", "")
        nationality = request.POST.get("nationality", "").strip()

        if name:
            Author.objects.create(
                name=name,
                birth_date=birth_date,
                nationality=nationality
            )
            return redirect("index_author")  


    return render(request, "authors/new.html")

def show_author(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    return render(request, "authors/show.html", {"author": author})