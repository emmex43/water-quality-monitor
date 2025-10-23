from flask import jsonify, request
from app.database.connection import db
from app.models.water_quality import WaterQuality
from flask_login import login_required, current_user

def init_water_routes(app):
    @app.route('/api/water/reading', methods=['POST'])
    @login_required
    def add_water_reading():
        """Add a new water quality reading"""
        try:
            data = request.json
            reading = WaterQuality(
                location_name=data.get('location_name'),
                ph_level=data.get('ph_level'),
                turbidity_ntu=data.get('turbidity_ntu'),
                dissolved_oxygen=data.get('dissolved_oxygen'),
                temperature_c=data.get('temperature_c'),
                conductivity_us=data.get('conductivity_us'),
                user_id=current_user.id  # Link to current user
            )
            
            db.session.add(reading)
            db.session.commit()
            
            return jsonify({
                'message': 'Water quality reading added successfully!',
                'reading_id': reading.id
            }), 201
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400
    
    @app.route('/api/water/readings', methods=['GET'])
    @login_required
    def get_water_readings():
        """Get all water quality readings for current user"""
        try:
            readings = WaterQuality.query.filter_by(user_id=current_user.id).order_by(WaterQuality.timestamp.desc()).all()
            result = [reading.to_dict() for reading in readings]
            
            return jsonify({
                'readings': result,
                'count': len(result)
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/water/public-readings', methods=['GET'])
    def get_public_readings():
        """Get public water quality readings (no authentication required)"""
        try:
            readings = WaterQuality.query.order_by(WaterQuality.timestamp.desc()).limit(10).all()
            result = [reading.to_dict() for reading in readings]
            
            return jsonify({
                'readings': result,
                'count': len(result),
                'message': 'Public water quality data'
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500