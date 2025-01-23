import tkinter as tk
from tkinter import ttk
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
        self.window.geometry("800x600")
        self.window.resizable(False, False)

        # Style and theme
        self.style = ttk.Style(self.window)
        self.style.theme_use("clam")

        # Custom colors
        self.style.configure("TFrame", background="#f5f5f5")
        self.style.configure("TLabel", background="#f5f5f5", font=("Arial", 12))
        self.style.configure("TButton", font=("Arial", 10), padding=5)

        # Load icons
        self.book_icon = tk.PhotoImage(file="icons/book.png")  # Replace with your icon path
        self.history_icon = tk.PhotoImage(file="icons/history.png")
        self.admin_icon = tk.PhotoImage(file="icons/admin.png")
        self.logout_icon = tk.PhotoImage(file="icons/logout.png")

        # Show login screen
        self.show_login_screen()

        self.window.mainloop()

    def show_login_screen(self):
        # Clear existing widgets
        for widget in self.window.winfo_children():
            widget.destroy()

        # Login screen layout
        frame = ttk.Frame(self.window, padding=20)
        frame.pack(expand=True)

        ttk.Label(frame, text="Library Management System", font=("Arial", 24), background="#f5f5f5").pack(pady=10)
        ttk.Label(frame, text="Login", font=("Arial", 16), background="#f5f5f5").pack(pady=5)

        ttk.Label(frame, text="Name:").pack(pady=5)
        self.name_entry = ttk.Entry(frame, width=30)
        self.name_entry.pack(pady=5)

        ttk.Button(frame, text="Login", command=self.login_user).pack(pady=10)
        ttk.Button(frame, text="Register", command=self.register_user).pack(pady=5)

    def login_user(self):
        name = self.name_entry.get()
        for user in self.library.users:
            if user.name.lower() == name.lower():
                self.current_user = user
                self.create_main_tabs()
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

    def create_main_tabs(self):
        # Clear existing widgets
        for widget in self.window.winfo_children():
            widget.destroy()

        # Create tabbed interface
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill="both", expand=True)

        # Add tabs with icons
        self.create_books_tab(notebook)
        self.create_history_tab(notebook)
        if self.current_user.is_admin:
            self.create_admin_tab(notebook)

        # Logout button
        logout_button = ttk.Button(
            self.window, text="Logout", image=self.logout_icon, compound="left", command=self.show_login_screen
        )
        logout_button.pack(pady=10)

    def create_books_tab(self, notebook):
        books_tab = ttk.Frame(notebook, padding=10)
        notebook.add(books_tab, text="Books", image=self.book_icon, compound="left")

        ttk.Label(books_tab, text="Books Available", font=("Arial", 16)).pack(pady=10)

        # Book list
        book_list = tk.Text(books_tab, height=20, width=70, bg="#e8e8e8")
        book_list.pack(pady=10)
        book_list.insert("1.0", "\n".join(str(book) for book in self.library.books))
        book_list.configure(state="disabled")

        # Action buttons
        actions_frame = ttk.Frame(books_tab)
        actions_frame.pack(pady=10)

        ttk.Button(actions_frame, text="Borrow Book", command=self.borrow_books).grid(row=0, column=0, padx=5)
        ttk.Button(actions_frame, text="Return Book", command=self.return_books).grid(row=0, column=1, padx=5)

    def create_history_tab(self, notebook):
        history_tab = ttk.Frame(notebook, padding=10)
        notebook.add(history_tab, text="History", image=self.history_icon, compound="left")

        ttk.Label(history_tab, text="Borrowing History", font=("Arial", 16)).pack(pady=10)

        history_text = tk.Text(history_tab, height=20, width=70, bg="#e8e8e8")
        history_text.pack(pady=10)

        history = "\n".join(
            f"'{book.title}' by {book.author} - Borrowed: {book.borrowed_date}, Due: {book.due_date}"
            for book in self.current_user.borrowed_books
        )
        history_text.insert("1.0", history if history else "No borrowing history found.")
        history_text.configure(state="disabled")

    def create_admin_tab(self, notebook):
        admin_tab = ttk.Frame(notebook, padding=10)
        notebook.add(admin_tab, text="Admin", image=self.admin_icon, compound="left")

        ttk.Label(admin_tab, text="Admin Options", font=("Arial", 16)).pack(pady=10)

        # Admin actions
        ttk.Button(admin_tab, text="Add Book", command=self.add_book).pack(pady=5)
        ttk.Button(admin_tab, text="Remove Book", command=self.remove_book).pack(pady=5)
        ttk.Button(admin_tab, text="View All Users", command=self.view_users).pack(pady=5)

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
            self.library.borrow_book(title, self.current_user)

    def return_books(self):
        title = askstring("Return Book", "Enter the title of the book to return:")
        if title:
            self.library.return_book(title, self.current_user)
        
   
    def add_book(self):
        title = askstring("Add Book", "Enter the title of the book:")
        author = askstring("Add Book", "Enter the author of the book:")
        if title and author:
            self.library.add_book(Book(title, author), self.current_user)

    def remove_book(self):
        title = askstring("Remove Book", "Enter the title of the book to remove:")
        if title:
            self.library.remove_book(title, self.current_user)

    def view_users(self):
        users_info = "\n".join([f"{user.name} - {'Admin' if user.is_admin else 'User'}" for user in self.library.users])
        self.display_message(users_info)

    

    def display_message(self, message):
        messagebox.showinfo("Library Info", message)



library = Library("City Library")
library.load_data()

admin = User("Admin", is_admin=True)


if admin not in library.users:
    library.users.append(admin)


LibraryGUI(library)
