# LIBRARY-API

### Creating an API for a library using MySql as a database managing members and books

---

## How to run MySql on Docker

#### `To create the container and run`
```
docker run --name mysql \
    -e MYSQL_ROOT_PASSWORD=<your password>  \
    -e MYSQL_DATABASE=library_db \
    -p 3306:3306 \
    -d mysql:8
```
#### `To run the container if it exist`
```
docker exec -it mysql mysql -u root -p
```

---

## Directory Structure
```
library-api/
│
├── app/
│   └── main.py
│
├── database/
│   ├── book_db.py
│   ├── db_connection.py
│   └── report_routes.py
│
├── routes/
│   ├── book_routes.py
│   ├── member_routes.py
│   └── report_routes.py
│
├── logs/
│   └── app.log
│
├── requirements.txt
└── README.md
```
- `app/` - where the web app is running 
- `database/` - where all the data is stored
- `routes/` - the end point for the server
- `logs/` - logging
---
## Table Structure


### `Books Table`
| Field | Type | Attributes | Description |
| :--- | :--- | :--- | :--- | 
| `id` | INT | PK, AUTO INCREMENT| book ID|
| `title` | VARCHAR(50) | NOT NULL| book name|
|`author` | VARCHAR(50) | NOT NULL| author name|
| `genre` | ENUM (Fiction, Non-Fiction, Science, HistoryOther) | NOT NULL | book genre |
| `is_available` | BOOLEAN | NOT NULL | book available?|
| `borrowed_by_member_id` | INT | DEFAULT NULL | id of the member that borrowed, if NULL it's available |

### `Members Table`

| Field | Type | Attributes | Description |
| :--- | :--- | :--- | :--- | 
| `id` | INT | PK, AUTO INCREMENT| member ID|
| `name` | VARCHAR(50) | NOT NULL| member name|
|`email` | VARCHAR(50) | UNIQUE, NOT NULL| member email |
| `is_active` | BOOLEAN | NOT NULL | member active? if false he can't borrow |
| `total_borrows` | INT | NOT NULL , DEFAULT 0 | up by one with each borrow |
---

## Rules

| Rule | Description |
| :--- | :--- |
creating new book | user sends `title/author/genre` system adds `is_available=TRUE`, `borrowed_by=NULL` |
| genre | must be ` Fiction / Non-Fiction / Science / History / Other` else the system send an error |
| creating new member | user sends ` email/name` system adds `is_active=TRUE, total_borrow=0`|
| email | must be unique if ,exist in system = error |
| inactive member | if `is_active=FALSE` can not borrow a book |
| not available book | can not borrow `is_available=FALSE`|
| max books | a member can not borrow more than 3 books at the same time |
| returning a book | each member can return only books assigned to himself |
---

## Endpoints

### `Books`

| Method | Endpoint | description |
| :--- | :--- | :--- |
| POST | /books | creating a book |
| GET | /books | all books |
| GET | /books/{id} | book by ID |
| PATCH | /books/{id} | update book |
| PATCH | /books/{id}/borrow/{member_id} | borrowing book to member |
| PATCH | /books/{id}/return/{member_id} | returning book from member |

### `Members`

| Method | Endpoint | description |
| :--- | :--- | :--- |
| POST | /members | creating a member |
| GET | /members | all members |
| GET | /members/{id} | member by ID |
| PATCH | /members/{id} | update member |
| PATCH | /members/{id}/deactivate | deactivate member |
| PATCH | /members/{id}/activate | activate member |

### `Reports`
| Method | Endpoint | description |
| :--- | :--- | :--- |
| GET | /reports/summary | general reports |
| GET | /reports/books-by-genre | books by report |
| GET | /reports/top-member | most active member |


## System Flow

The client send HTTP requests to the server (run by uvicorn)
the fastapi server get them to his endpoints functions and do what needs to be done in the MySql database

## How to run
- Create a virtual environment
```
# windows

python -m venv .venv
./.venv/Scripts/activate
```
```
# macOS/linux

python3 -m venv .venv
source .venv/bin/activate

```
- install requirements
```
pip install -r requirements.txt
```
- Run `python main.py`  to activate the server
```
cd <where the project is>/library-api
python main.py
```

