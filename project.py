""" A Library Management System to manage books, users, and borrowing activities. 

Problem Statement:
.A Library contains books.
.Books can be added to the library.
.Users can borrow and return books.
.The system should track which books are available and which are borrowed.
"""
import json
from datetime import datetime, timedelta


class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.is_borrowed = False
        self.borrowed_date = None
        self.due_date = None

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "is_borrowed": self.is_borrowed,
            "borrowed_date": self.borrowed_date.isoformat() if self.borrowed_date else None,
            "due_date": self.due_date.isoformat() if self.due_date else None,
        }

    @staticmethod
    def from_dict(data):
        book = Book(data["title"], data["author"])
        book.is_borrowed = data["is_borrowed"]
        book.borrowed_date = datetime.fromisoformat(data["borrowed_date"]) if data["borrowed_date"] else None
        book.due_date = datetime.fromisoformat(data["due_date"]) if data["due_date"] else None
        return book

    def __str__(self):
        status = "Available" if not self.is_borrowed else f"Borrowed (Due: {self.due_date})"
        return f"'{self.title}' by {self.author} - {status}"


class User:
    def __init__(self, name, is_admin=False):
        self.name = name
        self.is_admin = is_admin
        self.borrowed_books = []

    def to_dict(self):
        return {
            "name": self.name,
            "is_admin": self.is_admin,
            "borrowed_books": [book.to_dict() for book in self.borrowed_books],
        }

    @staticmethod
    def from_dict(data):
        user = User(data["name"], data["is_admin"])
        user.borrowed_books = [Book.from_dict(book) for book in data["borrowed_books"]]
        return user

    def display_borrowed_books(self):
        print(f"\n{self.name}'s Borrowed Books:")
        if not self.borrowed_books:
            print("No books borrowed.")
        else:
            for book in self.borrowed_books:
                print(book)


class Library:
    def __init__(self, name):
        self.name = name
        self.books = []
        self.users = []
        self.fine_per_day = 10

    def save_data(self):
        data = {
            "books": [book.to_dict() for book in self.books],
            "users": [user.to_dict() for user in self.users],
        }
        with open("library_data.json", "w") as f:
            json.dump(data, f, indent=4)
        print("Library data saved.")

    def load_data(self):
        try:
            with open("library_data.json", "r") as f:
                data = json.load(f)
                self.books = [Book.from_dict(book) for book in data["books"]]
                self.users = [User.from_dict(user) for user in data["users"]]
                print("Library data loaded.")
        except FileNotFoundError:
            print("No saved data found. Starting fresh.")

    def add_book(self, book, admin):
        if admin.is_admin:
            self.books.append(book)
            print(f"Added '{book.title}' to the library.")
        else:
            print("Only admins can add books.")

    def remove_book(self, title, admin):
        if admin.is_admin:
            for book in self.books:
                if book.title.lower() == title.lower():
                    self.books.remove(book)
                    print(f"Removed '{book.title}' from the library.")
                    return
            print(f"No book found with title '{title}'.")
        else:
            print("Only admins can remove books.")

    def search_books(self, keyword):
        print(f"\nSearch results for '{keyword}':")
        found = False
        for book in self.books:
            if keyword.lower() in book.title.lower() or keyword.lower() in book.author.lower():
                print(book)
                found = True
        if not found:
            print("No books found.")

    def display_books(self):
        print(f"\nBooks in {self.name}:")
        for book in self.books:
            print(book)

    def borrow_book(self, title, user):
        for book in self.books:
            if book.title.lower() == title.lower() and not book.is_borrowed:
                book.is_borrowed = True
                book.borrowed_date = datetime.now()
                book.due_date = book.borrowed_date + timedelta(days=7)
                user.borrowed_books.append(book)
                print(f"'{book.title}' has been borrowed by {user.name}. Due date: {book.due_date}.")
                return
        print(f"Sorry, '{title}' is not available.")

    def return_book(self, title, user):
        for book in user.borrowed_books:
            if book.title.lower() == title.lower():
                book.is_borrowed = False
                user.borrowed_books.remove(book)
                overdue_days = (datetime.now() - book.due_date).days
                fine = max(0, overdue_days * self.fine_per_day)
                book.borrowed_date = None
                book.due_date = None
                print(f"'{book.title}' has been returned by {user.name}.")
                if fine > 0:
                    print(f"Late return! Fine amount: ${fine}")
                else:
                    print("Returned on time. No fine.")
                return
        print(f"{user.name} doesn't have '{title}' to return.")


# Example Usage
library = Library("City Library")
library.load_data()

admin = User("Admin", is_admin=True)
user = User("Jonathan")

library.users.append(admin)
library.users.append(user)

# Adding and searching books as admin
library.add_book(Book("1984", "George Orwell"), admin)
library.add_book(Book("The Great Gatsby", "F. Scott Fitzgerald"), admin)
library.search_books("great")

# Borrowing and returning books
library.borrow_book("1984", user)
library.return_book("1984", user)

# Save library data
library.save_data()
 

        
    

        
      
    
    
  