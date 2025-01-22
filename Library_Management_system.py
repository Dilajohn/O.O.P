import tkinter as tk
from tkinter import messagebox
from tkinter.simpledialog import askstring

from project import Book, Library, User


class LibraryGUI:
    def __init__(self, library):
        self.library = library
        self.current_user = None

        # Create main window
        self.window = tk.Tk()
        self.window.title("Library Management System")
        self.window.geometry("600x400")

        # Start with login screen
        self.show_login_screen()

        # Create frames
        self.create_main_frame()

        self.window.mainloop()

    def show_login_screen(self):
        # Clear existing widgets
        for widget in self.window.winfo_children():
            widget.destroy()

        # Login screen layout
        tk.Label(self.window, text="Library Management System", font=("Arial", 20)).pack(pady=10)
        tk.Label(self.window, text="Login", font=("Arial", 16)).pack(pady=5)

        tk.Label(self.window, text="Name:").pack(pady=5)
        self.name_entry = tk.Entry(self.window)
        self.name_entry.pack(pady=5)

        tk.Button(self.window, text="Login", command=self.login_user).pack(pady=10)
        tk.Button(self.window, text="Register", command=self.register_user).pack(pady=5)

    def login_user(self):
        name = self.name_entry.get()
        for user in self.library.users:
            if user.name.lower() == name.lower():
                self.current_user = user
                self.create_main_frame()
                return
        messagebox.showerror("Error", f"User '{name}' not found. Please register first.")

    def register_user(self):
        name = self.name_entry.get()
        if not name:
            messagebox.showerror("Error", "Name cannot be empty!")
            return

        for user in self.library.users:
            if user.name.lower() == name.lower():
                messagebox.showerror("Error", "User already exists!")
                return

        new_user = User(name)
        self.library.users.append(new_user)
        self.library.save_data()
        messagebox.showinfo("Success", f"User '{name}' registered successfully! You can now log in.")

    def create_main_frame(self):
        # Clear existing widgets
        for widget in self.window.winfo_children():
            widget.destroy()

        # Main menu
        tk.Label(self.window, text=f"Welcome, {self.current_user.name}!", font=("Arial", 16)).pack(pady=10)

        # Buttons
        tk.Button(self.window, text="View All Books", command=self.view_books).pack(pady=5)
        tk.Button(self.window, text="Search Books", command=self.search_books).pack(pady=5)
        tk.Button(self.window, text="Borrow Books", command=self.borrow_books).pack(pady=5)
        tk.Button(self.window, text="Return Books", command=self.return_books).pack(pady=5)


        if self.current_user.is_admin:
            tk.Button(self.window, text="Admin Options", command=self.admin_options).pack(pady=5)

        tk.Button(self.window, text="View Borrowing History", command=self.view_borrowing_history).pack(pady=5)
        tk.Button(self.window, text="Logout", command=self.show_login_screen).pack(pady=10)


    def view_borrowing_history(self):
        history = "\n".join(
            f"'{book.title}' by {book.author} - Borrowed: {book.borrowed_date}, Due: {book.due_date}"
            for book in self.current_user.borrowed_books
        )
        self.display_message(history if history else "No borrowing history found.")



    def view_books(self):
        self.display_message("\n".join(str(book) for book in self.library.books))

    def search_books(self):
        keyword = askstring("Search Books", "Enter a title or author to search:")
        if keyword:
            results = [
                str(book)
                for book in self.library.books
                if keyword.lower() in book.title.lower() or keyword.lower() in book.author.lower()
            ]
            self.display_message("\n".join(results) if results else "No books found.")

    def borrow_books(self):
        title = askstring("Borrow Book", "Enter the title of the book to borrow:") 
        if title:
            user = self.select_user()
            if user:
                self.library.borrow_book(title, user)

    def return_books(self):
        title = askstring("Return Book", "Enter the title of the book to return:")
        if title:
            user = self.select_user()
            if user:
                self.library.return_book(title, user)

    def admin_options(self):
        # Admin menu
        admin_window = tk.Toplevel(self.window)
        admin_window.title("Admin Options")
        admin_window.geometry("400x300")

        tk.Label(admin_window, text="Admin Options", font=("Arial", 16)).pack(pady=10)

        tk.Button(admin_window, text="Add Book", command=self.add_book).pack(pady=5)
        tk.Button(admin_window, text="Remove Book", command=self.remove_book).pack(pady=5)
        tk.Button(admin_window, text="View All Users", command=self.view_users).pack(pady=5)

    def add_book(self):
        title = askstring("Add Book", "Enter the title of the book:")
        author = askstring("Add Book", "Enter the author of the book:")
        if title and author:
            admin = self.select_user(is_admin=True)
            if admin:
                self.library.add_book(Book(title, author), admin)

    def remove_book(self):
        title = askstring("Remove Book", "Enter the title of the book to remove:")
        if title:
            admin = self.select_user(is_admin=True)
            if admin:
                self.library.remove_book(title, admin)

    def view_users(self):
        users_info = "\n".join([f"{user.name} - {'Admin' if user.is_admin else 'User'}" for user in self.library.users])
        self.display_message(users_info)

    def select_user(self, is_admin=False):
        user_name = askstring("Select User", "Enter your name:")
        if user_name:
            for user in self.library.users:
                if user.name.lower() == user_name.lower():
                    if is_admin and not user.is_admin:
                        messagebox.showerror("Error", "You do not have admin privileges!")
                        return None
                    return user
            messagebox.showerror("Error", f"User '{user_name}' not found.")
        return None

    def display_message(self, message):
        messagebox.showinfo("Library Info", message)




library = Library("City Library")
library.load_data()

admin = User("Admin", is_admin=True)
user = User("Jonathan")

if admin not in library.users:
    library.users.append(admin)
if user not in library.users:
    library.users.append(user)

LibraryGUI(library)
