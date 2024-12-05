# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 11:34:22 2024

@author: meiss
"""

from library_system import Book, Library, Student


book = Book("1984", "George Orwell")
assert book.title == "1984"
assert book.author == "George Orwell"
assert book.is_available is True
assert str(book) == "1984 by George Orwell - Available"
print("Book tests passed!")



library = Library()
library.add_book("1984", "George Orwell")
library.add_book("Brave New World", "Aldous Huxley")
books = library.list_books()
assert len(books) == 2
assert "1984 by George Orwell - Available" in books
print("Library tests passed!")

library = Library()
library.add_book("1984", "George Orwell")

student = Student("John Doe")
result = student.borrow_book("1984", library)
assert result is True
assert "1984 by George Orwell" in student.borrowed_books

result = student.return_book("1984", library)
assert result is True
assert not student.borrowed_books
print("Student tests passed!")