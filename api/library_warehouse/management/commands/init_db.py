from django.core.management.base import BaseCommand
from library_warehouse.models import Book, Borrower

BORROWERS = [
    {"card_number": "100001", "name": "Jan Kowalski"},
    {"card_number": "100002", "name": "Anna Nowak"},
]

BOOKS = [
    {"serial_number": "200001", "title": "Django REST w pigułce", "author": "A. Dev"},
    {"serial_number": "200002", "title": "Clean Code", "author": "Robert C. Martin"},
]


class Command(BaseCommand):

    def handle(self, *args, **options):
        created_borrowers = 0
        for borrower in BORROWERS:
            _, created = Borrower.objects.get_or_create(
                card_number=borrower["card_number"],
                defaults={"name": borrower["name"]},
            )
            created_borrowers += int(created)

        created_books = 0
        for book in BOOKS:
            _, created = Book.objects.get_or_create(
                serial_number=book["serial_number"],
                defaults={"title": book["title"], "author": book["author"]},
            )
            created_books += int(created)

        self.stdout.write(
            self.style.SUCCESS(f"✅ DB init: borrowers +{created_borrowers}, books +{created_books} (idempotentnie).")
        )
