from functools import wraps
from flask import jsonify, redirect, url_for, flash, request
from flask_login import current_user
import json

def role_required(role_name):
    """Decorator to require specific role for route access"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                if request.accept_mimetypes.accept_json:
                    return jsonify({'error': 'Authentication required'}), 401
                return redirect(url_for('auth.login'))
            
            if not current_user.has_role(role_name):
                if request.accept_mimetypes.accept_json:
                    return jsonify({'error': 'Insufficient permissions'}), 403
                flash('Access denied: Insufficient permissions', 'error')
                return redirect(url_for('main.dashboard'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Specific role decorators for convenience
def admin_required(f):
    return role_required('admin')(f)

def researcher_required(f):
    return role_required('researcher')(f)

def government_required(f):
    return role_required('government')(f)

def community_or_above_required(f):
    """Any authenticated user (community member or above)"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            if request.accept_mimetypes.accept_json:
                return jsonify({'error': 'Authentication required'}), 401
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function