from django.db import models
from authors.models import Author
from datetime import datetime
from categories.models import Category

def validate_number_of_books_available_less_than_possessed(self):
    return self.number_of_books_available < self.number_of_book_possessed
    
def validate_publication_year(self):        
    current_year = datetime.now().year
    if not (1450 <= self.published_date.year <= current_year):
        raise ValueError("L'année de publication doit être comprise entre 1450 et l'année courante.")

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    published_date = models.DateField(validators=[ validate_publication_year ])
    price = models.DecimalField(max_digits=6, decimal_places=2)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    number_of_books_available = models.PositiveIntegerField(default=0, validators=[ validate_number_of_books_available_less_than_possessed ])
    number_of_book_possessed = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="books")
    langage = models.CharField(max_length=50, blank=True)
    number_of_pages = models.PositiveIntegerField(null=True, blank=True)
    house_of_edition = models.CharField(max_length=100, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
