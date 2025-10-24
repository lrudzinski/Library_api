from django.db import models


class Borrower(models.Model):
    name = models.CharField(max_length=100)
    card_number = models.CharField(max_length=100, primary_key=True, unique=True)


class Book(models.Model):
    serial_number = models.CharField(max_length=6, primary_key=True, unique=True)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    is_borrowed = models.BooleanField(default=False)
    borrowed_at = models.CharField(max_length=100, blank=True, null=True)
    borrowed_by = models.ForeignKey(
        Borrower, null=True, blank=True, on_delete=models.SET_NULL, related_name="borrowed_books"
    )

    def __str__(self):
        return f"{self.serial_number} - {self.title}"
