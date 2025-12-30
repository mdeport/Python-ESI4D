from django import forms
from ..models import Author

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = [
            "first_name",
            "last_name",
            "birth_date",
            "nationality",
            "biography",
            "date_dead",
            "url_reference",
        ]
        widgets = {
            "birth_date": forms.DateInput(attrs={"type": "date"}),
            "date_dead": forms.DateInput(attrs={"type": "date"}),
            "biography": forms.Textarea(attrs={"rows": 4}),
        }