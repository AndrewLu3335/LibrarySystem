from flask import Blueprint, request, jsonify
from library_backend.service.book_service import BookService
from library_backend.service.user_service import UserService 
bp = Blueprint("api", __name__)
bs = BookService()
us = UserService()

@bp.route("/books", methods=["GET"])
def get_books():
    """get all books' info

    Returns:
        JSON: _all books' info_
    """
    books = bs.get_all_books()
    return jsonify(books)

@bp.route("/books/<int:user_id>", methods=["GET"])
def get_book_by_user(user_id):
    """get all books borrowed by a user

    Args:
        user_id (int): _user id_

    Returns:
        JSON: _user's borrowed books_
    """
    books = bs.get_books_by_user(user_id)
    return jsonify(books)

@bp.route("/add_book", methods=["POST"])
def add_book():
    """add a book

    tittle + author

    Returns:
        JSON: _new book's info_
    """
    return jsonify(bs.add_book(request.get_json())), 201

@bp.route("/borrow", methods=["POST"])
def borrow_book():
    """borrow a book
        book_id
    Returns:
        JSON: _borrow result_
    """
    return bs.borrow_book(request.get_json())

@bp.route("/return", methods=["POST"])
def return_book():
    """return a book
        book_id, user_id
    Returns:
        JSON: _return result_
    """
    print("Return request received with data:", request.get_json())
    return bs.return_book(request.get_json())

@bp.route("/modify", methods=["PUT"])
def modify_book():
    """modify book info

    Returns:
        JSON: modify result
    """
    print("Modify request received with data:", request.get_json())
    return bs.modify_book(request.get_json())

@bp.route("/withdraw", methods=["DELETE"])
def withdraw_book():
    """withdraw a book

    Returns:
        JSON: withdraw result
    """
    book_id = request.args.get("book_id", type=int)
    print("Withdraw request received with book_id:", book_id)
    return bs.withdraw_book(book_id)

