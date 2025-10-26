from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def init_database(app):
    """Initialize SQLAlchemy and Flask-Login."""
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    with app.app_context():
        try:
            # Only create tables if the connection works
            db.create_all()
            print(f"✅ Database connected: {app.config['SQLALCHEMY_DATABASE_URI']}")
            return True
        except Exception as e:
            print(f"❌ Database setup failed: {e}")
            return False


@login_manager.user_loader
def load_user(user_id):
    """Load user for Flask-Login."""
    from app.models.user import User
    try:
        return User.query.get(int(user_id))
    except Exception as e:
        print(f"⚠️ Error loading user: {e}")
        return None
