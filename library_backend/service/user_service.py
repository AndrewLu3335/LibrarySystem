from library_backend.repository.user_repo import UserRepo
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash


class UserService:
    def __init__(self):
        self.user_repository = UserRepo()
    
    def login(self, user_data):
        """Authenticate a user by username and password.

        Args:
            user_data (dict): A dictionary containing user credentials.
            eg. {"name": "John Doe", "password": "password123"}

        Returns:
            dict: The authenticated user's information or an error message.
        """
        # Check if input is valid
        if not user_data or "name" not in user_data or "password" not in user_data:
            return {"error": "Invalid input: 'name' and 'password' are required."}, 400
        # Query user by name
        user = self.user_repository.get_user_by_name(user_data["name"])
        if not user:
            return {"error": "User not found"}, 404
        # Validate password using hash
        if not check_password_hash(user.password, user_data["password"]):
            return {"error": "Invalid password"}, 401
        # Login successful, return user id and role
        return {"message": "Login successful", "user_id": user.id, "name": user.name, "role": user.role}, 200

    def add_user(self, user_data):
        """Add a new user to the system.

        Args:
            user_data (dict): A dictionary containing user information.
            eg. {"name": "John Doe"}

        Returns:
            dict: The newly created user's information.
        """
        if not user_data or "name" not in user_data or "password" not in user_data:
            raise ValueError("Invalid input: 'name' and 'password' are required.")
        # Hash the password before storing it
        user_data["password"] = generate_password_hash(user_data["password"])
        return self.user_repository.add_user(user_data)

    # def get_user_by_id(self, user_id):
    #     return self.user_repository.get_user_by_id(user_id)

   

    # def update_user(self, user_id, user_data):
    #     return self.user_repository.update_user(user_id, user_data)

    # def delete_user(self, user_id):
    #     return self.user_repository.delete_user(user_id)