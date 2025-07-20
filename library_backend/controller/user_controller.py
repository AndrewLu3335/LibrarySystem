from flask import Blueprint, request, jsonify
from library_backend.service.user_service import UserService
bp_user = Blueprint("user_api", __name__)
us = UserService()

@bp_user.route("/login", methods=["POST"])
def login():
    """User login endpoint.

    Returns:
        JSON: User authentication result.
    """
    print("Login request received with data:", request.get_json())
    return us.login(request.get_json())

@bp_user.route("/add_user", methods=["POST"])
def add_user():
    """add a user

    Returns:
        JSON: add result
    """
    return us.add_user(request.get_json())