from flask import jsonify, request, session, render_template, redirect, url_for
from app.database.connection import db
from app.models.user import User
from flask_login import login_user, logout_user, login_required, current_user

def init_auth_routes(app):
    # ===== TEMPLATE ROUTES =====
    @app.route('/login')
    def login_page():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        return render_template('login.html')
    
    @app.route('/register')
    def register_page():
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
        return redirect(url_for('login_page'))

    # ===== API ROUTES =====
    @app.route('/api/auth/register', methods=['POST'])
    def api_register():
        try:
            data = request.json
            print(f"📝 Registration attempt for: {data.get('email')}")
            
            # Check if user already exists
            if User.query.filter_by(email=data.get('email')).first():
                return jsonify({'error': 'Email already registered'}), 400
            
            # Create new user
            user = User(
                name=data.get('name'),
                email=data.get('email'),
                address=data.get('address'),
                telephone=data.get('telephone'),
                organization=data.get('organization', ''),
                role=data.get('role', 'community')
            )
            user.set_password(data.get('password'))
            
            db.session.add(user)
            db.session.commit()
            
            print(f"✅ User registered: {user.email}")
            return jsonify({
                'message': 'User registered successfully!',
                'user': user.to_dict()
            }), 201
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Registration error: {e}")
            return jsonify({'error': str(e)}), 400
    
    @app.route('/api/auth/login', methods=['POST'])
    def api_login():
        try:
            data = request.json
            print(f"🔐 Login attempt for: {data.get('email')}")
            
            user = User.query.filter_by(email=data.get('email')).first()
            
            if user and user.check_password(data.get('password')):
                login_user(user)
                session['user_id'] = user.id
                print(f"✅ Login successful: {user.email}")
                return jsonify({
                    'message': 'Login successful!',
                    'user': user.to_dict()
                })
            else:
                print(f"❌ Login failed: {data.get('email')}")
                return jsonify({'error': 'Invalid email or password'}), 401
                
        except Exception as e:
            print(f"❌ Login error: {e}")
            return jsonify({'error': str(e)}), 400
    
    @app.route('/api/auth/logout', methods=['POST'])
    @login_required
    def api_logout():
        logout_user()
        session.pop('user_id', None)
        print("✅ User logged out")
        return jsonify({'message': 'Logout successful!'})
    
    @app.route('/api/auth/me', methods=['GET'])
    @login_required
    def api_get_current_user():
        return jsonify({'user': current_user.to_dict()})
    
    @app.route('/api/auth/check', methods=['GET'])
    def api_check_auth():
        if current_user.is_authenticated:
            return jsonify({'authenticated': True, 'user': current_user.to_dict()})
        else:
            return jsonify({'authenticated': False})