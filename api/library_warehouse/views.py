import re

from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Book, Borrower
from .serializers import BookSerializer, BorrowerSerializer


class BorrowerViewSet(viewsets.ModelViewSet):
    queryset = Borrower.objects.all()
    serializer_class = BorrowerSerializer
    http_method_names = ["get", "post", "put", "patch", "delete"]


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    http_method_names = ["get", "post", "put", "patch", "delete"]

    @action(detail=True, methods=["patch"])
    def borrow(self, request, pk=None):
        book = self.get_object()
        if book.is_borrowed:
            return Response({"error": "This book is already borrowed."}, status=status.HTTP_409_CONFLICT)

        card = request.data.get("borrower_card_number")
        if not card or not re.fullmatch(r"\d{6}", str(card)):
            return Response(
                {"error": "Provide a valid borrower_card_number (6 digits)."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            borrower = Borrower.objects.get(pk=card)
        except Borrower.DoesNotExist:
            return Response({"error": "No borrower found with this card number."}, status=status.HTTP_404_NOT_FOUND)

        book.is_borrowed = True
        book.borrowed_by = borrower
        book.borrowed_at = timezone.now()
        book.save(update_fields=["is_borrowed", "borrowed_by", "borrowed_at"])
        return Response(BookSerializer(book).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["patch"])
    def return_book(self, request, pk=None):
        book = self.get_object()
        if not book.is_borrowed or book.borrowed_by is None:
            return Response({"error": "This book is not currently borrowed."}, status=status.HTTP_409_CONFLICT)

        card = request.data.get("borrower_card_number")
        if not card or not re.fullmatch(r"\d{6}", str(card)):
            return Response(
                {"error": "Provide a valid borrower_card_number (6 digits)."}, status=status.HTTP_400_BAD_REQUEST
            )

        if book.borrowed_by.card_number != card:
            return Response({"error": "This book was borrowed by another borrower."}, status=status.HTTP_403_FORBIDDEN)

        book.is_borrowed = False
        book.borrowed_by = None
        book.borrowed_at = None
        book.save(update_fields=["is_borrowed", "borrowed_by", "borrowed_at"])
        return Response(BookSerializer(book).data, status=status.HTTP_200_OK)
