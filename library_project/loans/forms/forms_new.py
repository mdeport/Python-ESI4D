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
            "comments": forms.Textarea(attrs={"rows": 3}),
        }

    def clean(self):
        cleaned = super().clean()
        book = cleaned.get("book")
