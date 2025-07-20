from library_backend.models import BorrowRecord
from library_backend.app import db
from datetime import datetime
from sqlalchemy import desc

class BorrowRecordRepo:
    def add_borrow_record(self, data):
        """Insert a borrow record into the database.

        Args:
            data (dict): Contains user_id and book_id.

        Returns:
            dict: The borrow record information.
        """
        borrow_record = BorrowRecord(user_id=data["user_id"], book_id=data["book_id"], borrow_date=datetime.now())
        db.session.add(borrow_record)
        return {"user_id": borrow_record.user_id, "book_id": borrow_record.book_id}, 201

    def query_borrow_record(self, data):
        """Query latest borrow record by user_id and book_id.

        Args:
            data (dict): Contains user_id and book_id.

        Returns:
            BorrowRecord: The borrow record if found, otherwise None.
        """
        return BorrowRecord.query.filter_by(user_id=data["user_id"], book_id=data["book_id"]).order_by(desc(BorrowRecord.borrow_date)).first()
    
    def get_borrow_records_by_user_and_status(self, user_id, returned=None):
        """
        Query borrow records by user_id and optionally by returned status.
        If returned is not None, filter by returned status.
        """
        query = BorrowRecord.query.filter_by(user_id=user_id)
        if returned is not None:
            query = query.filter_by(returned=returned)
        return query.all()

    def update_borrow_record(self, record, **kwargs):
        """Update a borrow record.

        Args:
            record_id (int): The ID of the borrow record.
            **kwargs: Fields to update.

        Returns:
            dict: The updated borrow record information.
        """
        valid_properties = ["user_id", "book_id", "borrow_date", "returned", "return_date"]
        if not record:
            return {"error": "Borrow record not found"}, 404
        for key, value in kwargs.items():
            setattr(record, key, value)
        return {"id": record.id, "user_id": record.user_id, "book_id": record.book_id, "borrow_date": record.borrow_date}, 200