from django import forms
from ..models import Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "description"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
            "name": forms.TextInput(attrs={"class": "form-control"}),
        }

    def clean_name(self):
        name = self.cleaned_data.get("name", "").strip()
        if not name:
            raise forms.ValidationError("Le nom de la catégorie est requis.")
        return name