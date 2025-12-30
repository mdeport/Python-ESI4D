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
            "birth_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "date_dead": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "biography": forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "nationality": forms.TextInput(attrs={"class": "form-control"}),
            "url_reference": forms.URLInput(attrs={"class": "form-control"})
        }