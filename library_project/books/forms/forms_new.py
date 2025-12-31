from django import forms
from ..models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            "title",
            "isbn",
            "published_date",
            "price",
            "author",
            "number_of_book_possessed",
            "number_of_books_available",
            "description",
            "category",
            "langage",
            "number_of_pages",
            "house_of_edition",
        ]
        widgets = {
            "published_date": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "isbn": forms.TextInput(attrs={"class": "form-control"}),
            "price": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "author": forms.Select(attrs={"class": "form-control"}),
            "number_of_book_possessed": forms.NumberInput(attrs={"class": "form-control"}),
            "number_of_books_available": forms.NumberInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "langage": forms.TextInput(attrs={"class": "form-control"}),
            "number_of_pages": forms.NumberInput(attrs={"class": "form-control"}),
            "house_of_edition": forms.TextInput(attrs={"class": "form-control"}),
        }

    def clean(self):
        cleaned = super().clean()
        avail = cleaned.get("number_of_books_available")
        poss = cleaned.get("number_of_book_possessed")

        if avail is not None and poss is not None and avail > poss:
            self.add_error(
                "number_of_books_available",
                "Le nombre d'exemplaires disponibles ne peut pas dépasser le nombre total possédé."
            )
        return cleaned