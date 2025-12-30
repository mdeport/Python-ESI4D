from django import forms
from django.utils import timezone
from ..models import Loan

class LoanChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        # affiche Nom Emprunteur — Titre du livre
        return f"{obj.name_borrower} — {obj.book.title}"

class LoanReturnForm(forms.ModelForm):
    loan = LoanChoiceField(
        queryset=Loan.objects.filter(date_returned__isnull=True).select_related("book"),
        label="Emprunt actif",
        required=True
    )

    date_returned = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
        label="Date de retour (laisser vide = aujourd'hui)"
    )

    class Meta:
        model = Loan
        fields = ["date_returned", "comments"]
        widgets = {
            "date_returned": forms.DateTimeInput(attrs={"type": "datetime-local", "class": "form-control"}),
            "comments": forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
        }

    def clean_loan(self):
        loan = self.cleaned_data["loan"]
        if loan.date_returned is not None:
            raise forms.ValidationError("Cet emprunt est déjà retourné.")
        return loan

    def clean_date_returned(self):
        dt = self.cleaned_data.get("date_returned")
        if dt is None:
            return timezone.now()
        if timezone.is_naive(dt):
            return timezone.make_aware(dt)
        return dt