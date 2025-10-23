from flask import jsonify
from app.database.connection import db
from flask_login import current_user

def init_main_routes(app):
    @app.route('/')
    def hello_sdg():
        return jsonify({
            'message': 'Water Quality API running successfully! 💧',
            'status': 'active', 
            'project': 'SDG 6 - Clean Water and Sanitation',
            'purpose': 'Monitor water quality parameters for safe water access',
            'authentication': 'User system enabled'
        })
    
    @app.route('/health')
    def health_check():
        try:
            # Test database connection with SQLAlchemy
            db.session.execute('SELECT 1')
            auth_status = current_user.is_authenticated if hasattr(current_user, 'is_authenticated') else False
            
            return jsonify({
                'status': 'healthy',
                'database': 'connected',
                'authentication': 'active',
                'user_authenticated': auth_status,
                'message': 'Water quality monitoring system operational! ✅'
            })
        except Exception as e:
            return jsonify({
                'status': 'unhealthy',
                'database': 'disconnected',
                'error': str(e)
            }), 500
    
    @app.route('/api/test-db')
    def test_database():
        """Test database connection"""
        try:
            db.session.execute('SELECT 1')
            return jsonify({
                'status': 'success',
                'message': 'Database connection working!'
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': f'Database connection failed: {str(e)}'
            }), 500