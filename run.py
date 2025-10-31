import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # ✅ Get port from Render
    print("🚀 Starting Water Quality Monitoring API...")
    print("💧 SDG 6: Clean Water and Sanitation")
    print(f"📍 Access the web interface at: http://0.0.0.0:{port}")
    print(f"📱 Dashboard: http://0.0.0.0:{port}/dashboard")
    print(f"📊 Analytics: http://0.0.0.0:{port}/analytics/dashboard")
    app.run(debug=False, host='0.0.0.0', port=port)