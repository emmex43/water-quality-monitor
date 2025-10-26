from app import create_app

app = create_app()

if __name__ == '__main__':
    print("🚀 Starting Water Quality Monitoring API...")
    print("💧 SDG 6: Clean Water and Sanitation")
    print("📍 Access the web interface at: http://localhost:5000")
    print("📱 Dashboard: http://localhost:5000/dashboard")
    print("📊 Analytics: http://localhost:5000/analytics/dashboard")
    app.run(debug=False, host='0.0.0.0', port=5000)  # ✅ Changed debug=True to debug=False