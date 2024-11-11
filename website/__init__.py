from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path

# Initialize database and login manager
db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    db.init_app(app)
    
    from .views import views
    from .auth import auth
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User  # Import models here

    create_db(app)

    # Initialize the login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # Redirect to the login page if not logged in
    login_manager.init_app(app)  # Initialize with the app

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app

def create_db(app):
    """Creates the database if it doesn't exist."""
    if not path.exists(f"website/{DB_NAME}"):
        with app.app_context():
            db.create_all()
            print("Created Database!")
