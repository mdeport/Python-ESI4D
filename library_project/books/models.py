from django.db import models
from django.forms import ValidationError
from authors.models import Author
from datetime import date
from categories.models import Category

def validate_publication_year(value):
    current_year = date.today().year
    if not (1450 <= value.year <= current_year):
        raise ValidationError("L'année de publication doit être comprise entre 1450 et l'année courante.")

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    published_date = models.DateField(validators=[ validate_publication_year ])
    price = models.DecimalField(max_digits=6, decimal_places=2)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    number_of_books_available = models.PositiveIntegerField(default=0)
    number_of_book_possessed = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="books")
    langage = models.CharField(max_length=50, blank=True)
    number_of_pages = models.PositiveIntegerField(null=True, blank=True)
    house_of_edition = models.CharField(max_length=100, blank=True)
    date_added = models.DateField(auto_now_add=True)


    def clean(self):
        errors = {}
        if (self.number_of_books_available is not None and
                self.number_of_book_possessed is not None and
                self.number_of_books_available > self.number_of_book_possessed):
            errors["number_of_books_available"] = "Le nombre d'exemplaires disponibles ne peut pas dépasser le total possédé."
        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return self.title
