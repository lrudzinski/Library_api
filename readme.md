# 📚 Library Warehouse API

The **Library Warehouse API** is a simple backend for managing books and borrowers.  
It allows creating, editing, deleting, borrowing, and returning books.  
The project is containerized using **Docker** and uses **PostgreSQL** as its database.  


## ⚙️ Tech Stack

- **Python 3.12**  
- **Django 5.x**  
- **Django REST Framework (DRF)**  
- **PostgreSQL**  
- **Docker & Docker Compose**  
- **Pytest** (for testing)

## Books

| Action     | Method      | Endpoint                              |
| ----------- | ------------ | ------------------------------------- |
| List all    | GET          | /api/books/                           |
| Create      | POST         | /api/books/                           |
| Retrieve    | GET          | /api/books/<serial_number>/           |
| Update      | PATCH / PUT  | /api/books/<serial_number>/           |
| Delete      | DELETE       | /api/books/<serial_number>/           |
| Borrow      | PATCH        | /api/books/<serial_number>/borrow/    |
| Return      | PATCH        | /api/books/<serial_number>/return_book/ |

## Borrowers

| Action     | Method      | Endpoint                              |
| ----------- | ------------ | ------------------------------------- |
| List all    | GET          | /api/borrowers/                       |
| Create      | POST         | /api/borrowers/                       |
| Retrieve    | GET          | /api/borrowers/<card_number>/         |
| Update      | PATCH / PUT  | /api/borrowers/<card_number>/         |
| Delete      | DELETE       | /api/borrowers/<card_number>/         |



## 📁 Project Structure

```bash
library_warehouse/
├── library_warehouse/       # main Django project folder
├── api/                     # app with views, models, serializers
├── tests/                   # pytest test suite
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md


## Install build project
```bash
docker compose up --build
```

## Create book
```bash
curl -X POST http://localhost:8000/api/books/ \
  -H "Content-Type: application/json" \
  -d '{"serial_number":"200001","title":"Django REST","author":"A. Dev"}'

```
## Borrow a Book
```bash
curl -X PATCH http://localhost:8000/api/books/200001/borrow/ \
  -H "Content-Type: application/json" \
  -d '{"borrower_card_number":"100001"}'
```
## Return a Book
```bash
curl -X PATCH http://localhost:8000/api/books/200001/return_book/ \
  -H "Content-Type: application/json" \
  -d '{"borrower_card_number":"100001"}'
```

## Run tests
```bash
docker exec -it <container_name_id python> bash 
nox -s test
```