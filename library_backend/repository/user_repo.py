from library_backend.models import User
from library_backend.app import db
from datetime import datetime
from flask import jsonify
from library_backend.util.decorators import db_transaction


class UserRepo:

    def validate_user(self, data):
        """Validate user credentials.

        Args:
            data (dict): Contains 'name' and 'password'.

        Returns:
            dict: User information if valid, else None.
        """
        user = User.query.filter_by(name=data["name"], password=data["password"]).first()
        return user if user else None
    

    def add_user(self,data):
        # validate input
        if not data or "name" not in data:
            return jsonify({"message": "Invalid input"}), 400
        user = User(name=data["name"])
        # insert user into database
        db.session.add(user)
        return jsonify({"message": "User added successfully", "user_name": user.name}), 201
    
    def get_user_by_id(self, user_id):
        """Get user by ID.

        Args:
            user_id (int): The ID of the user.

        Returns:
            dict: User information.
        """
        user = User.query.get(user_id)
        return {"id": user.id, "name": user.name}, 200
    
    def get_user_by_name(self, name):
        """Get user by name (return SQLAlchemy user object)."""
        return User.query.filter_by(name=name).first()
