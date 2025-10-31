from flask import Flask
from app.config import Config
from app.database.connection import init_database, db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize database first
    if init_database(app):
        # Import models INSIDE app context to avoid circular imports
        with app.app_context():
            from app.models.user import User  # ✅ Import User FIRST
            from app.models.water_quality import WaterQuality
            db.create_all()  # Now both tables exist
    
    print("🔄 Starting route registration...")
    
    # Initialize all routes
    from app.routes.main import init_main_routes
    from app.routes.water import init_water_routes  
    from app.routes.auth import init_auth_routes
    from app.routes.analytics import analytics_bp
    
    init_main_routes(app)
    init_water_routes(app)
    init_auth_routes(app)
    app.register_blueprint(analytics_bp, url_prefix='/analytics')
    
    print("✅ All routes registered successfully!")
    return app