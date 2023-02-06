#========Module imports==========
from tabulate import tabulate
import sqlite3
db = sqlite3.connect('ebookstore')
cursor = db.cursor()

#========Database Init===========
# Create table "books" with relevant columns
cursor.execute('''CREATE TABLE IF NOT EXISTS
    books(id INTEGER PRIMARY KEY, title TEXT, author TEXT, qty INTEGER)''')
db.commit()

# Error handling for IntegrityError. Rolls back to previous commit if exception
# raised
try:
    # Inserting data into table via executemany
    book_data = [
        (3001, 'A Tale of Two Cities', 'Charles Dickens', 30), 
        (3002, "Harry Potter and the Philosopher's Stone", 'J.K. Rowling', 40), 
        (3003, 'The Lion, the Witch and the Wardrobe', 'C.S. Lewis', 25), 
        (3004, 'The Lord of the Rings', 'J.R.R Tolkien', 37), 
        (3005, 'Alice in Wonderland', 'Lewis Carroll', 12), 
    ]
    cursor.executemany('''INSERT INTO books(id, title, author, qty) VALUES(?, ?, ?, ?)''', 
    book_data)
    db.commit()
except sqlite3.IntegrityError:
    db.rollback()
    pass

#==========Functions=============
# Add new books to the database
def add_book():
    while True:
        try:
            # Ask user input for data & insert into 'books' table
            id = int(input("Enter ID of new book: "))
            title = input("Enter title of new book: ")
            author = input("Enter author of new book: ")
            qty = int(input("Enter quantity of new book: "))

            cursor.execute('''INSERT INTO books(id, title, author, qty) VALUES(?, ?, ?, ?)''', 
                (id, title, author, qty))
            db.commit()
        
        # Error handling if user inputs text instead of an int for id & qty
        except ValueError:
            print("\033[31mThat is an invalid input. Please try again.\033[0m\n")
            continue 

        # Error handling if user inputs an existing ID in database
        except sqlite3.IntegrityError:
            print("\033[31mBook ID already exists in database. Please input another book ID.\033[0m\n")
            continue
        else:
            print("\nNew book successfully added to the database 🎉\n")
            break

# View all books in database in table display format
def view_all():
    cursor.execute('''SELECT * FROM books''')
    all_books = cursor.fetchall()

    # Display database in table format
    headers = [f"\033[1m{i[0].title()}\033[0m" for i in cursor.description]
    table = tabulate(all_books, headers=headers, tablefmt='fancy_grid')
    print(table)

# Update book information
def update_book():
    while True:
        # Error handling if user inputs text instead of an int for id
        try:
            id = int(input("\nEnter ID of the book you'd like to update: "))
        except ValueError:
            print("\033[31m\nThat is an invalid option. Please try again.\033[0m")
            continue
        else:
            pass

        # Select book data based on ID, & display to user if exists. If not, 
        # prompt again
        cursor.execute('''SELECT * FROM books WHERE id=?''', (id,))
        book = cursor.fetchone()
        if book is None:
            print(f"\n\033[31mBook ID {id} does not exist in database. Please try again.\033[0m")
            continue
        else:
            headers = ["Id", "Title", "Author", "Qty"]
            table = tabulate([book], headers=headers, tablefmt='fancy_grid')
            print(table + "\n")

        # Confirm if user would like to proceed with update. If no, return to 
        # main menu. Else prompt user again
        while True:
            confirmation = input("Would you like to update this book record (Y/N)? ").strip().upper()
            if confirmation == "Y":
                while True:
                    try:
                        # Ask user input for updated fields
                        new_title = input("Enter updated title: ")
                        new_author = input("Enter updated author: ")
                        new_qty = int(input("Enter updated quantity: "))

                        cursor.execute('''UPDATE books SET title = ?, author = ?, qty = ? WHERE id = ?''', 
                            (new_title, new_author, new_qty, id))
                        db.commit()
                    
                    # Error handling if user inputs text instead of an int for qty
                    except ValueError:
                        print("\033[31mThat is an invalid input. Please try again.\033[0m\n")
                        continue 
                    # Error handling if user inputs an existing ID in database
                    except sqlite3.IntegrityError:
                        print("\033[31mBook ID already exists in database. Please input another book ID.\033[0m\n")
                        continue
                    else:
                        print("\033[0;32m\nBook successfully updated in the database 🎉\033[0m\n")
                        return

            elif confirmation == "N":
                print()
                return
            else:
                print(f"\n\033[31m'{confirmation}' is not a valid input. Please enter 'Y' or 'N'.\033[0m\n")
                continue

# Delete books from database
def delete_book():
    while True:
        # Error handling if user inputs text instead of an int for id
        try:
            id = int(input("\nEnter ID of the book you'd like to delete: "))
        except ValueError:
            print("\033[31m\nThat is an invalid option. Please try again.\033[0m")
            continue
        else:
            pass

        # Select book data based on ID, & display to user if exists. If not, 
        # prompt again
        cursor.execute('''SELECT * FROM books WHERE id=?''', (id,))
        book = cursor.fetchone()
        if book is None:
            print(f"\n\033[31mBook ID {id} does not exist in database. Please try again.\033[0m")
            continue
        else:
            headers = ["Id", "Title", "Author", "Qty"]
            table = tabulate([book], headers=headers, tablefmt='fancy_grid')
            print(table + "\n")
        
        # Confirm if user would like to proceed with deletion. If no, return to 
        # main menu. Else prompt user again
        while True:
            confirmation = input("Would you like to delete this book record (Y/N)? ").strip().upper()
            if confirmation == "Y":
                cursor.execute('''DELETE FROM books WHERE id = ?''', 
                    (id,))
                db.commit()
                print("\033[0;32m\nBook successfully deleted from the database 🎉\033[0m\n")
                return
            elif confirmation == "N":
                print()
                return
            else:
                print(f"\n\033[31m'{confirmation}' is not a valid input. Please enter 'Y' or 'N'.\033[0m\n")
                continue

# Search database to find a specific book
def search_book():
    while True:
        # Ask user input whether they'd like to search by ID, title or author.
        # Other user inputs will prompt user again.
        request = input("\nWould you like to search by ID, title or author: ").strip().upper()

        # If request is id, validate id input
        if request == "ID":
            while True:
                try:
                    id_input = int(input("Please enter book ID: "))
                except ValueError:
                    print(f"\n\033[31mInvalid input. Please try again.\033[0m\n")
                    continue
                else:
                    break
            # If book ID matches with IDs in database, print in table format.
            # If no book found, prompt user again.
            cursor.execute('''SELECT * FROM books WHERE id = ?''', 
                (id_input,))
            book = cursor.fetchone()
            if book is None:
                print("\n\033[31mNo matches found in database. Please try again.\033[0m\n")
                continue
            else:
                headers = ["Id", "Title", "Author", "Qty"]
                table = tabulate([book], headers=headers, tablefmt='fancy_grid')
                print(table + "\n")
                return
        
        # If request is title...
        elif request == "TITLE":
            title_input = input("Please enter book title: ")
            cursor.execute('''SELECT * FROM books WHERE UPPER(title) = UPPER(?)''', 
                (title_input,))
            book = cursor.fetchall()
            # If no books found, prompt user again
            if len(book) == 0:
                print(f"\n\033[31mNo book found with the title '{title_input}'. Please try again.\033[0m")
                continue
            # If one book found, print in table format & return to main menu
            elif len(book) == 1:
                headers = ["Id", "Title", "Author", "Qty"]
                table = tabulate(book, headers=headers, tablefmt='fancy_grid')
                print(table + "\n")
                return
            # If many book found, print in table format & return to main menu
            else:
                headers = ["Id", "Title", "Author", "Qty"]
                table = tabulate(book, headers=headers, tablefmt='fancy_grid')
                print(table + "\n")
                return

        # If request is author...
        elif request == "AUTHOR":
            author_input = input("Please enter author name: ")
            cursor.execute('''SELECT * FROM books WHERE UPPER(author) = UPPER(?)''', 
                (author_input,))
            book = cursor.fetchall()
            # If no books found, prompt user again
            if len(book) == 0:
                print(f"\n\033[31mNo book found with the author '{author_input}'. Please try again.\033[0m")
                continue
            # If one book found, print in table format & return to main menu
            elif len(book) == 1:
                headers = ["Id", "Title", "Author", "Qty"]
                table = tabulate(book, headers=headers, tablefmt='fancy_grid')
                print(table + "\n")
                return
            # If many book found, print in table format & return to main menu
            else:
                headers = ["Id", "Title", "Author", "Qty"]
                table = tabulate(book, headers=headers, tablefmt='fancy_grid')
                print(table + "\n")
                return
        else:
            print("\n\033[31mThat is an invalid input. Please try again.\033[0m")
            continue

#==========Main Menu=============
# Welcome banner
print(
    "\033[35m┏" + ("▬" * 80) + "┓\033[0m\n"
    "\033[35m┃" + (" " * 80) + "┃\033[0m\n"
    "\033[35m┃" + (" " * 21)+ "\033[34m📚 Welcome to the bookstore database 📚" 
                + (" " * 20) + "\033[35m┃\033[0m\n"
    "\033[35m┃" + (" " * 80) + "┃\033[0m\n"
    "\033[35m┗" + ("▬" * 80) + "┛\033[0m\n"
)

while True:
    # Validate user input for main menu options
    try:
        menu = int(input(
            "\033[1m\033[4mPlease select from the following options (0-4):\033[0m\n\n"
            "\033[1;31m1. 📖 Enter book 📖\033[0m\n"
            "\033[33m2. 📝 Update book 📝\033[0m\n"
            "\033[32m3. 🗑  Delete book 🗑\033[0m\n"
            "\033[34m4. 🔎 Search books 🔎\033[0m\n"
            "\033[35m0. 🚪 Exit 🚪\033[0m\n"
        ))
    except ValueError:
        print("\033[31mThat is an invalid option. Please try again.\033[0m\n")
        continue
    else:
        pass

    # Menu routes & choices
    if menu == 1:
        add_book()
        view_all()
        continue

    elif menu == 2:
        view_all()
        update_book()
        continue

    elif menu == 3:
        view_all()
        delete_book()
        continue

    elif menu == 4:
        view_all()
        search_book()
        continue

    elif menu == 0:
        print("\033[1m\033[3m\n👋 Thank you for using the bookstore database. Goodbye! 👋\033[0m\n")
        db.close()
        exit()

    else:
        print("\033[31mThat is an invalid option. Please try again.\033[0m\n")
        continue