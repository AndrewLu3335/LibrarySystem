from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

from library_backend import db

def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    DB_DIR = os.path.abspath(os.path.dirname(__file__))
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(DB_DIR, 'library.db')}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    from library_backend.controller.book_controller import bp
    from library_backend.controller.user_controller import bp_user
    print("✅ Registering blueprint...")
    app.register_blueprint(bp, url_prefix='/api')
    app.register_blueprint(bp_user, url_prefix='/user') 
    print("✅ Blueprint registered.")
    with app.app_context():
        db.create_all()
    for rule in app.url_map.iter_rules():
        print(f"✅ Registered endpoint: {rule}")
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True,port=8000,host="0.0.0.0")


