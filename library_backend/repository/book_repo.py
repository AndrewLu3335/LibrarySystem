from library_backend.models import Book, BorrowRecord
from library_backend.app import db
from datetime import datetime
from flask import jsonify
from library_backend.util.decorators import db_transaction

class BookRepo:
    def get_books(self):
        """query all books info

        Returns:
            dict: all books info
        """
        books = Book.query.all()
        print(books)
        print({"id": b.id, "title": b.title, "author": b.author, "available": b.available} for b in books)
        return [{"id": b.id, "title": b.title, "author": b.author, "available": b.available} for b in books]
    
    def get_specific_book(self, book_id):
        """query a specific book info

        Args:
            book_id (int): book id

        Returns:
            dict: specific book info
        """
        book = Book.query.get(book_id)
        return {"id": book.id, "title": book.title, "author": book.author, "available": book.available}

    def create_book(self, data):
        """insert a data into book

        Args:
            data (dict): title and author

        Returns:
            dict: new book info
        """
        book = Book(title=data["title"], author=data["author"], available=0)
        db.session.add(book)
        print(f"✅ insert book success!  ", "title:" + str(book.title) + ", author:" + str(book.author) +", available:" + str(book.available) )
        return {"title": book.title, "author": book.author, "available": book.available}

    
    def update_book(self, **kwargs):
        """Update book information.

        Args:
            book_id (int): The ID of the book to update.
            **kwargs: The properties to update (e.g., title, author, available).

        Returns:
            dict: The updated book information.
        """
        valid_properties = ['title', 'author', 'available', 'book_id']
        print(kwargs)
        book = Book.query.get(kwargs.get("book_id"))
        if not book:
            return {"error": "Book not found"}, 404
        print(f"Updating book with ID {kwargs.get('book_id')} with data: {kwargs}")
        for key, value in kwargs.items():
            print(f"Processing key: {key}, value: {value}")
            if key in valid_properties:
                setattr(book, key, value)
                print(f"✅ update book success!  ", "title:" + str(book.title) + ", author:" + str(book.author) +", available:" + str(book.available) )
        return {"id": book.id, "title": book.title, "author": book.author, "available": book.available}, 200