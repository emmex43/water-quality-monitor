from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from app.models.water_quality import WaterQuality
from app.models.user import User
from app.middleware.auth import role_required, researcher_required, admin_required
from sqlalchemy import func, extract
from datetime import datetime, timedelta

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/dashboard')
@login_required
def analytics_dashboard():
    """Main analytics dashboard page"""
    return render_template('analytics_dashboard.html', user=current_user)

@analytics_bp.route('/api/statistics')
@login_required
def statistics():
    """Get basic statistics for dashboard cards"""
    try:
        # Base query with role-based filtering
        if current_user.can_view_all_data():
            base_query = WaterQuality.query
        else:
            base_query = WaterQuality.query.filter(
                (WaterQuality.user_id == current_user.id) | 
                (WaterQuality.is_public == True)
            )
        
        total_readings = base_query.count()
        excellent_readings = base_query.filter_by(status='excellent').count()
        avg_ph = base_query.with_entities(func.avg(WaterQuality.ph_level)).scalar() or 0
        active_locations = base_query.with_entities(WaterQuality.location_name).distinct().count()
        
        return jsonify({
            'total_readings': total_readings,
            'excellent_readings': excellent_readings,
            'avg_ph': float(avg_ph),
            'active_locations': active_locations
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/api/water-quality-trends')
@login_required
def water_quality_trends():
    """Get trend data for charts (last 30 days)"""
    try:
        print("📈 Trends API called...")
        
        # Base query with role-based filtering
        if current_user.can_view_all_data():
            query = WaterQuality.query
            print("   🔓 Using all data (researcher access)")
        else:
            query = WaterQuality.query.filter(
                (WaterQuality.user_id == current_user.id) | 
                (WaterQuality.is_public == True)
            )
            print("   🔒 Using filtered data (community access)")
        
        # Get all readings count first
        total_readings = query.count()
        print(f"   📊 Total readings available: {total_readings}")
        
        # If no data at all, return empty structure
        if total_readings == 0:
            print("   ⚠️  No data found, returning empty structure")
            return jsonify({
                'dates': [],
                'ph_values': [],
                'do_values': [], 
                'turbidity_values': [],
                'reading_counts': []
            })
        
        # Remove date filter temporarily to get all data for testing
        trends_data = query\
            .with_entities(
                func.date(WaterQuality.timestamp).label('date'),
                func.avg(WaterQuality.ph_level).label('avg_ph'),
                func.avg(WaterQuality.dissolved_oxygen).label('avg_do'),
                func.avg(WaterQuality.turbidity_ntu).label('avg_turbidity'),
                func.count(WaterQuality.id).label('reading_count')
            )\
            .group_by(func.date(WaterQuality.timestamp))\
            .order_by('date')\
            .all()
        
        print(f"   📈 Trend data points found: {len(trends_data)}")
        
        # If no trend data after grouping, create sample data from existing readings
        if not trends_data:
            print("   ⚠️  No trend data after grouping, creating from individual readings")
            # Get individual readings to create trend data
            individual_readings = query.order_by(WaterQuality.timestamp).all()
            
            dates = []
            ph_values = []
            do_values = []
            turbidity_values = []
            reading_counts = []
            
            for reading in individual_readings:
                dates.append(reading.timestamp.date().isoformat() if reading.timestamp else datetime.utcnow().date().isoformat())
                ph_values.append(float(reading.ph_level or 7.0))
                do_values.append(float(reading.dissolved_oxygen or 8.0))
                turbidity_values.append(float(reading.turbidity_ntu or 5.0))
                reading_counts.append(1)
            
            return jsonify({
                'dates': dates,
                'ph_values': ph_values,
                'do_values': do_values,
                'turbidity_values': turbidity_values,
                'reading_counts': reading_counts
            })
        
        # Process the grouped trend data - FIXED DATE HANDLING
        dates = []
        ph_values = []
        do_values = []
        turbidity_values = []
        reading_counts = []
        
        for row in trends_data:
            # FIX: Proper date handling - check if it's a date object or string
            if row.date and hasattr(row.date, 'isoformat'):
                # It's a date object
                dates.append(row.date.isoformat())
            elif row.date:
                # It's already a string
                dates.append(str(row.date))
            else:
                # No date, use current date
                dates.append(datetime.utcnow().date().isoformat())
            
            ph_values.append(float(row.avg_ph or 7.0))  # Default to neutral pH if null
            do_values.append(float(row.avg_do or 8.0))  # Default to good DO if null
            turbidity_values.append(float(row.avg_turbidity or 5.0))  # Default to good turbidity if null
            reading_counts.append(row.reading_count or 1)
        
        response_data = {
            'dates': dates,
            'ph_values': ph_values,
            'do_values': do_values,
            'turbidity_values': turbidity_values,
            'reading_counts': reading_counts
        }
        
        print(f"   ✅ Sending {len(dates)} data points")
        print(f"   📅 Sample dates: {dates[:3] if dates else 'None'}")
        return jsonify(response_data)
        
    except Exception as e:
        print(f"❌ Error in trends API: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': str(e),
            'dates': [],
            'ph_values': [],
            'do_values': [], 
            'turbidity_values': [],
            'reading_counts': []
        }), 500

@analytics_bp.route('/api/quality-distribution')
@login_required
def quality_distribution():
    """Get data for quality distribution pie chart"""
    try:
        if current_user.can_view_all_data():
            query = WaterQuality.query
        else:
            query = WaterQuality.query.filter(
                (WaterQuality.user_id == current_user.id) | 
                (WaterQuality.is_public == True)
            )
        
        distribution = query.with_entities(
            WaterQuality.status,
            func.count(WaterQuality.id).label('count')
        ).group_by(WaterQuality.status).all()
        
        # If no data, create default structure
        if not distribution:
            return jsonify({
                'labels': ['No Data'],
                'data': [1],
                'colors': ['#6c757d']
            })
        
        return jsonify({
            'labels': [row.status.title() if row.status else 'Unknown' for row in distribution],
            'data': [row.count for row in distribution],
            'colors': ['#28a745', '#20c997', '#ffc107', '#dc3545', '#6c757d']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/api/location-insights')
@login_required
@researcher_required
def location_insights():
    """Get detailed location insights (researcher+ only)"""
    try:
        locations_data = WaterQuality.query.with_entities(
            WaterQuality.location_name,
            func.avg(WaterQuality.ph_level).label('avg_ph'),
            func.avg(WaterQuality.dissolved_oxygen).label('avg_do'),
            func.avg(WaterQuality.turbidity_ntu).label('avg_turbidity'),
            func.count(WaterQuality.id).label('reading_count'),
            func.max(WaterQuality.timestamp).label('last_reading')
        ).group_by(WaterQuality.location_name).all()
        
        return jsonify([{
            'location': row.location_name,
            'avg_ph': float(row.avg_ph or 0),
            'avg_do': float(row.avg_do or 0),
            'avg_turbidity': float(row.avg_turbidity or 0),
            'reading_count': row.reading_count,
            'last_reading': row.last_reading.isoformat() if row.last_reading else None
        } for row in locations_data])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/api/user-statistics')
@login_required
@admin_required
def user_statistics():
    """Get user statistics (admin only)"""
    try:
        user_stats = User.query.with_entities(
            User.role,
            func.count(User.id).label('user_count'),
            func.avg(func.extract('epoch', func.now() - User.created_at) / 86400).label('avg_days_since_join')
        ).group_by(User.role).all()
        
        return jsonify([{
            'role': row.role,
            'user_count': row.user_count,
            'avg_days_since_join': float(row.avg_days_since_join or 0)
        } for row in user_stats])
    except Exception as e:
        return jsonify({'error': str(e)}), 500