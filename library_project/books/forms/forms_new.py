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
            "description": forms.Textarea(attrs={"rows": 4}),
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