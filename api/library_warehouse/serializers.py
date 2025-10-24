from django.db import IntegrityError, transaction
from rest_framework import serializers

from .models import Book, Borrower


class BorrowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrower
        fields = ["card_number", "name"]

    def create(self, validated_data):
        try:
            with transaction.atomic():
                return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({"card_number": ["This card number already exists."]})


class BookSerializer(serializers.ModelSerializer):
    borrowed_by = BorrowerSerializer(read_only=True)

    class Meta:
        model = Book
        fields = ["serial_number", "title", "author", "is_borrowed", "borrowed_by", "borrowed_at"]

    def create(self, validated_data):
        try:
            with transaction.atomic():
                return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({"serial_number": ["This serial number already exists."]})
