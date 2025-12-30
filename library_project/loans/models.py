from django.db import models
from books.models import Book
from django.db.models import Q

# Create your models here.
class Loan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="loans")
    name_borrower = models.CharField(max_length=100)
    mail_borrower = models.EmailField()
    number_of_card_librairies = models.CharField(max_length=50)
    date_loan = models.DateTimeField(auto_now_add=True)
    date_limit_return = models.DateTimeField(null=True, blank=True)
    date_returned = models.DateTimeField(null=True, blank=True)
    state_book_returned = models.CharField(max_length=100, blank=True)
    comments = models.TextField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["book"], condition=Q(date_returned__isnull=True), name="unique_active_loan_per_book"),
        ]

    def is_active(self):
        return self.date_returned is None

    def __str__(self):
        return f"Loan of book {self.book_id}"