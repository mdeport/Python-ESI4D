from django import forms
from ..models import Loan

class LoanNewForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = [
            "book",
            "name_borrower",
            "mail_borrower",
            "number_of_card_librairies",
            "comments",
        ]
        widgets = {
            "comments": forms.Textarea(attrs={"rows": 3,"class": "form-control"}),
            "book": forms.Select(attrs={"class": "form-control"}),
            "name_borrower": forms.TextInput(attrs={"class": "form-control"}),
            "mail_borrower": forms.EmailInput(attrs={"class": "form-control"}), 
            "number_of_card_librairies": forms.TextInput(attrs={"class": "form-control"}),
        }

    def clean(self):
        cleaned = super().clean()
        book = cleaned.get("book")

        if book:
            if getattr(book, "number_of_books_available", 0) <= 0:
                raise forms.ValidationError({"book": "Aucun exemplaire disponible pour ce livre."})
            
        return cleaned