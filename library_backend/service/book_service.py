from library_backend.repository.book_repo import BookRepo
from library_backend.repository.user_repo import UserRepo
from library_backend.repository.borrow_record_repo import BorrowRecordRepo
from library_backend.util.decorators import db_transaction
from datetime import datetime
UserRepo = UserRepo()
BookRepo = BookRepo()
BorrowRecordRepo = BorrowRecordRepo()

class BookService:

    def get_all_books(self):
        """Get all books' information.

        Returns:
            list: A list of all books' information.
        """
        return BookRepo.get_books()
    
    def get_books_by_user(self, user_id):
        """Get all books borrowed by a specific user (not yet returned).

        Args:
            user_id (int): The ID of the user.

        Returns:
            list: A list of books borrowed by the user and not yet returned.
        """
        if not user_id:
            return {"error": "Invalid input: 'user_id' is required."}, 400
        user = UserRepo.get_user_by_id(user_id)
        if user is None:
            return {"error": "User not found"}, 404
        # query borrow records by user_id and status (not returned)
        borrow_records = BorrowRecordRepo.get_borrow_records_by_user_and_status(user_id, returned=False)
        books = []
        for record in borrow_records:
            # record.book_id
            book = BookRepo.get_specific_book(record.book_id)
            if book:
                books.append(book)
        return books
   
    @db_transaction
    def add_book(self, data):
        print(f"Adding book with data: {data}")
        result = BookRepo.create_book(data)
        return result

    @db_transaction
    def borrow_book(self, data):
        """Borrow a book.

        Args:
            data (dict): Contains user_id and book_id.

        Returns:
            dict: The borrow record information.
        """
        user_id = data.get("user_id")
        book_id = data.get("book_id")
        # validate user_id and book_id
        if not user_id or not book_id:
            return {"error": "Invalid input: 'user_id' and 'book_id' are required."}, 400
        # check if user exists
        user = UserRepo.get_user_by_id(user_id)
        if user is None:
            return {"error": "User not found"}, 404
        # query book by id
        book = BookRepo.get_specific_book(book_id)
        # check if book exists
        if book is None:
            return {"error": "Book not found"}, 404
        # check if book is available
        if book["available"] in [0,2]:  # 0 means withdrawn, 2 means borrowed
            return {"error": "Book is not available"}, 400
        # update book's available status
        update_info = {"book_id": book_id, "available": 2}
        BookRepo.update_book(**update_info)
        # create a borrow record
        record = BorrowRecordRepo.add_borrow_record({"user_id": user_id, "book_id": book_id})
        # validate if the borrow record was created successfully
        if "error" in record:
            return record
        return record
    
    @db_transaction
    def return_book(self, data):
        """Return a borrowed book.

        Args:
            data (dict): Contains user_id and book_id.

        Returns:
            dict: The return result.
        """
        record = BorrowRecordRepo.query_borrow_record({'user_id': data['user_id'], 'book_id': data['book_id']})
        BorrowRecordRepo.update_borrow_record(record, returned=True, return_date=datetime.now())
        update_info = {"book_id": data['book_id'], "available": 1}
        BookRepo.update_book(**update_info)
        return {"message": "Book returned successfully"}, 200
    
    @db_transaction
    def modify_book(self,data):
        """Modify book information.

        Args:
            data (dict): Contains book_id and fields to update.

        Returns:
            dict: The updated book information.
        """
        book_id = data.get("book_id")
        # Validate input
        if not data or not book_id:
            return {"error": "Invalid input: 'book_id' is required."}, 400     
        return BookRepo.update_book( **data)
    
    @db_transaction
    def withdraw_book(self,book_id):
        """Withdraw a book from the library.

        Args:
            book_id (int): The ID of the book to withdraw.

        Returns:
            dict: The result of the withdrawal operation.
        """
        # Validate input
        if not book_id:
            return {"error": "Invalid input: 'book_id' is required."}, 400
        # Check if book exists
        book = BookRepo.get_specific_book(book_id)
        if not book:
            return {"error": "Book not found"}, 404
        # Withdraw the book
        update_info = {"book_id": book_id, "available": 0}
        BookRepo.update_book(**update_info)  # 0 means withdrawn
        return {"message": "Book withdrawn successfully"}, 200



      