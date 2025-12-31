from django.shortcuts import render, redirect, get_object_or_404
from .models import Category
from .forms.forms_new import CategoryForm

def index_category(request):
    categories = Category.objects.all()
    return render(request, "categories/index.html", {"categories": categories})

def new_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("index_category")
    else:
        form = CategoryForm()
    return render(request, "categories/new.html", {"form": form})

def show_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    return render(request, "categories/show.html", {"category": category})

def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect("show_category", category_id=category.id)
    else:
        form = CategoryForm(instance=category)
    return render(request, "categories/edit.html", {"form": form, "category": category})