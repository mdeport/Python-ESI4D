from django.db import models
from django.db.models import UniqueConstraint
from django.core.exceptions import ValidationError

# Create your models here.
class Author(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    birth_date = models.DateField()
    nationality = models.CharField(max_length=100)
    biography = models.TextField(blank=True)
    date_dead = models.DateField(null=True, blank=True)
    url_reference = models.URLField(blank=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["first_name", "last_name"], name="unique_author_fullname"),
        ]
    

    def delete(self, *args, **kwargs):
        if hasattr(self, "books") and self.books.exists():
            raise ValidationError("Impossible de supprimer : des livres sont associés à cet auteur.")
        return super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"