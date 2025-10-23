from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def init_database(app):
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    
    # Create tables
    with app.app_context():
        try:
            db.create_all()
            print("✅ Database connected and tables created!")
            return True
        except Exception as e:
            print(f"❌ Database setup failed: {e}")
            return False

@login_manager.user_loader
def load_user(user_id):
    from app.models.user import User
    return User.query.get(int(user_id))