from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from config import Config

# Initialize extensions
db = SQLAlchemy()  # Database initialization
bcrypt = Bcrypt()  # Password hashing
login_manager = LoginManager()  # Flask-Login initialization
login_manager.login_view = "auth.login"  # Default login view
login_manager.login_message_category = "info"  # Flash message category

# Application Factory
def create_app():
    """
    Application factory for creating Flask app instances.
    This function initializes extensions and registers blueprints.
    """
    app = Flask(__name__)
    app.config.from_object(Config)  # Load configuration from Config class

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Flask-Login user loader
    @login_manager.user_loader
    def load_user(user_id):
        """
        This function is used by Flask-Login to load a user from the database.
        """
        from app.models import User  # Import here to avoid circular import issues
        return User.query.get(int(user_id))

    # Register blueprints
    from app.routes import auth, main
    app.register_blueprint(auth, url_prefix='/auth')  # All 'auth' routes prefixed with '/auth'
    app.register_blueprint(main)  # 'main' routes have no prefix

    return app





