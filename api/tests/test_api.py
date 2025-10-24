import pytest
from django.utils import timezone
from library_warehouse.models import Book, Borrower
from rest_framework.test import APIClient

BOOKS_LIST = "/api/books/"
BORROWERS_LIST = "/api/borrowers/"


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
@pytest.mark.django_db
def borrower_jan_fixture():
    return Borrower.objects.create(card_number="100001", name="Jan Kowalski")


@pytest.fixture
@pytest.mark.django_db
def borrower_anna_fixture():
    return Borrower.objects.create(card_number="100002", name="Anna Nowak")


@pytest.fixture
@pytest.mark.django_db
def book_clean_fixture():
    return Book.objects.create(serial_number="200001", title="Clean Code", author="Robert C. Martin")


@pytest.fixture
@pytest.mark.django_db
def borrowed_book_fixture(borrower_jan_fixture):
    book = Book.objects.create(
        serial_number="200002",
        title="Django REST",
        author="A. Dev",
        is_borrowed=True,
        borrowed_by=borrower_jan_fixture,
        borrowed_at=timezone.now(),
    )
    return book


@pytest.mark.django_db
def test_create_book(client):
    payload = {"serial_number": "300001", "title": "Two Scoops", "author": "Greenfeld"}
    result = client.post(BOOKS_LIST, payload, format="json")
    assert result.status_code in {200, 201}
    assert result.data["serial_number"] == "300001"
    assert result.data["title"] == "Two Scoops"


@pytest.mark.django_db
def test_list_books(client, book_clean_fixture):
    result = client.get(BOOKS_LIST)
    assert result.status_code == 200
    assert any(b["serial_number"] == "200001" for b in result.json())


@pytest.mark.django_db
def test_retrieve_book(client, book_clean_fixture):
    result = client.get(f"{BOOKS_LIST}{book_clean_fixture.serial_number}/")
    assert result.status_code == 200
    assert result.data["author"] == "Robert C. Martin"


@pytest.mark.django_db
def test_update_book_patch(client, book_clean_fixture):
    result = client.patch(
        f"{BOOKS_LIST}{book_clean_fixture.serial_number}/", {"title": "Clean Code (PL)"}, format="json"
    )
    assert result.status_code == 200
    assert result.data["title"] == "Clean Code (PL)"


@pytest.mark.django_db
def test_delete_book(client, book_clean_fixture):
    delete_result = client.delete(f"{BOOKS_LIST}{book_clean_fixture.serial_number}/")
    assert delete_result.status_code in {200, 204}
    get_result = client.get(f"{BOOKS_LIST}{book_clean_fixture.serial_number}/")
    assert get_result.status_code == 404


@pytest.mark.django_db
def test_borrow_book_success(client, book_clean_fixture, borrower_jan_fixture):
    result = client.patch(
        f"{BOOKS_LIST}{book_clean_fixture.serial_number}/borrow/",
        {"borrower_card_number": borrower_jan_fixture.card_number},
        format="json",
    )
    assert result.status_code == 200
    assert result.data["is_borrowed"] is True
    assert result.data["borrowed_by"]["card_number"] == borrower_jan_fixture.card_number


@pytest.mark.django_db
def test_borrow_book_already_borrowed(client, borrowed_book_fixture, borrower_anna_fixture):
    result = client.patch(
        f"{BOOKS_LIST}{borrowed_book_fixture.serial_number}/borrow/",
        {"borrower_card_number": borrower_anna_fixture.card_number},
        format="json",
    )
    assert result.status_code == 409
    assert "this book is already borrowed" in result.data["error"].lower()


@pytest.mark.django_db
def test_return_book_success(client, borrowed_book_fixture):
    result = client.patch(
        f"{BOOKS_LIST}{borrowed_book_fixture.serial_number}/return_book/",
        {"borrower_card_number": "100001"},
        format="json",
    )
    assert result.status_code == 200
    assert result.data["is_borrowed"] is False
    assert result.data["borrowed_by"] is None


@pytest.mark.django_db
def test_return_book_wrong_borrower_forbidden(client, borrowed_book_fixture):
    result = client.patch(
        f"{BOOKS_LIST}{borrowed_book_fixture.serial_number}/return_book/",
        {"borrower_card_number": "999999"},
        format="json",
    )
    assert result.status_code == 403
    assert "this book was borrowed by another borrower." in result.data["error"].lower()


@pytest.mark.django_db
def test_borrow_validation_invalid_card(client, book_clean_fixture):
    result = client.patch(
        f"{BOOKS_LIST}{book_clean_fixture.serial_number}/borrow/",
        {"borrower_card_number": "ABCDEF"},
        format="json",
    )
    assert result.status_code == 400


@pytest.mark.django_db
def test_create_borrower(client):
    result = client.post(BORROWERS_LIST, {"card_number": "123456", "name": "Test User"}, format="json")
    assert result.status_code in {200, 201}
    assert result.data["card_number"] == "123456"


@pytest.mark.django_db
def test_update_borrower(client, borrower_jan_fixture):
    client.post(BORROWERS_LIST, {"card_number": "123456", "name": "Test User"}, format="json")
    result = client.patch(f"{BORROWERS_LIST}{borrower_jan_fixture.card_number}/", {"name": "Jan K."}, format="json")
    assert result.status_code == 200
    assert result.data["name"] == "Jan K."


@pytest.mark.django_db
def test_book_serial_unique_violation_returns_400(client):
    payload = {"serial_number": "200001", "title": "Django REST", "author": "A. Dev"}
    post_action = client.post(BOOKS_LIST, payload, format="json")
    assert post_action.status_code in {200, 201}
    result = client.post(BOOKS_LIST, payload, format="json")
    assert result.status_code == 400
    assert "serial_number" in result.json()


@pytest.mark.django_db
def test_borrower_card_unique_violation_returns_400(client):
    payload = {"card_number": "100001", "name": "John Doe"}
    post_action = client.post(BORROWERS_LIST, payload, format="json")
    assert post_action.status_code in {200, 201}
    result = client.post(BORROWERS_LIST, payload, format="json")
    assert result.status_code == 400
    assert "card_number" in result.json()
