# Bookstore-Database
This Python program serves as a backend stock SQLite database for a bookstore. The user is able to add new books, update book information, delete books, & search from the database to find a specific book.

## Install
- `pip install tabulate` for formatting tables to display database information

## Database Initialisation
The 'books' table is created if it does not exist, with columns 'id', 'title', 'author', and 'qty' representing the book's ID number, title, author, and quantity respectively. Data is then inserted into the table using 'executemany'.

## Usage
After the relevant components have been installed, run:
```
$ python ebookstore.py
```
The following output will then be shown:

<img width="575" alt="image" src="https://user-images.githubusercontent.com/108587190/217044408-08309b9d-81c4-4436-b6e0-07f3967dee1e.png">
