# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 11:30:29 2024

@author: meiss
"""

class Book:
    def __init__(self, title: str, author: str):
        self.title = title
        self.author = author
        self.is_available = True

    def __str__(self):
        return f"{self.title} by {self.author} - {'Available' if self.is_available else 'Not Available'}"
    
class Library:
    def __init__(self):
        self.books = []

    def add_book(self, title: str, author: str):
        self.books.append(Book(title, author))

    def list_books(self) -> list:
        return [str(book) for book in self.books]

    def load_books(self, file_path: str):
        try:
            with open(file_path, "r") as file:
                for line in file:
                    title, author = line.strip().split(",")
                    self.add_book(title, author)
        except FileNotFoundError:
            print(f"File {file_path} not found.")

    def save_books(self, file_path: str):
        with open(file_path, "w") as file:
            for book in self.books:
                status = "1" if book.is_available else "0"
                file.write(f"{book.title},{book.author},{status}\n")

    def lend_book(self, book_title: str, student) -> bool:
        for book in self.books:
            if book.title == book_title and book.is_available:
                if book.title in student.borrowed_books:
                    print(f"{student.name} already borrowed this book.")
                    return False
                if len(student.borrowed_books) >= 3:
                    print(f"{student.name} has reached the borrowing limit.")
                    return False
                book.is_available = False
                student.borrowed_books.append(book_title)
                return True
        print("Book is not available.")
        return False

    def accept_return(self, book_title: str, student):
        for book in self.books:
            if book.title == book_title:
                if book_title in student.borrowed_books:
                    book.is_available = True
                    student.borrowed_books.remove(book_title)
                    return
                print("This book was not borrowed by the student.")
                return
        print("Book not found in the library.")

    def search_books(self, query: str) -> list:
        return [str(book) for book in self.books if query.lower() in book.title.lower() or query.lower() in book.author.lower()]
    
class Student:
    def __init__(self, name: str):
        self.name = name
        self.borrowed_books = []

    def borrow_book(self, book_title: str, library: Library):
        if library.lend_book(book_title, self):
            print(f"{self.name} borrowed {book_title}.")
        else:
            print(f"Could not borrow {book_title}.")

    def return_book(self, book_title: str, library: Library):
        library.accept_return(book_title, self)

def run_library_system():
    library = Library()
    library.load_books("library_data.txt")
    students = {}

    while True:
        print("\nLibrary System Menu:")
        print("1. View all books")
        print("2. Search for a book")
        print("3. Add a new book")
        print("4. Borrow a book")
        print("5. Return a book")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            books = library.list_books()
            print("\n".join(books) if books else "No books in the library.")

        elif choice == "2":
            query = input("Enter search query (title/author): ")
            results = library.search_books(query)
            print("\n".join(results) if results else "No matching books found.")

        elif choice == "3":
            title = input("Enter book title: ")
            author = input("Enter book author: ")
            library.add_book(title, author)
            print(f"Book '{title}' by {author} added to the library.")

        elif choice == "4":
            student_name = input("Enter student name: ")
            book_title = input("Enter the book title to borrow: ")
            if student_name not in students:
                students[student_name] = Student(student_name)
            students[student_name].borrow_book(book_title, library)

        elif choice == "5":
            student_name = input("Enter student name: ")
            book_title = input("Enter the book title to return: ")
            if student_name in students:
                students[student_name].return_book(book_title, library)
            else:
                print("Student not found.")

        elif choice == "6":
            library.save_books("library_data.txt")
            print("Library state saved. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")
