from library_backend.app import db
from functools import wraps


def db_transaction(func):
    """
    Decorator to handle database transactions.
    Rolls back the transaction in case of an exception.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            print
            result = func(*args, **kwargs)
            db.session.commit()
            print("✅ Transaction committed successfully")
            return result
        except Exception as e:
            db.session.rollback()
            print(f"❌ Transaction failed: {e}")
            return {"message": "Failed", "error": str(e)}, 500
    return wrapper