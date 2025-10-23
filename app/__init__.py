from flask import Flask, render_template, redirect, url_for
from app.config import Config
from app.database.connection import init_database, db
from app.routes.main import init_main_routes
from app.routes.water import init_water_routes
from app.routes.auth import init_auth_routes
from flask_login import current_user, login_required, logout_user

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize database and authentication
    if init_database(app):
        # Create tables
        with app.app_context():
            from app.models.water_quality import WaterQuality
            db.create_all()
    
    # Initialize all routes
    init_main_routes(app)
    init_water_routes(app)
    init_auth_routes(app)
    
    # Template routes
    @app.route('/login')
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        return render_template('login.html')
    
    @app.route('/register')
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        return render_template('register.html')
    
    @app.route('/dashboard')
    @login_required
    def dashboard():
        return render_template('dashboard.html', user=current_user)
    
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))
    
    return app