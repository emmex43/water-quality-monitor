import os
import sys

print("=== DEBUGGING APP PACKAGE ===\n")

# Test 1: Can we import the app package?
try:
    import app
    print("✅ SUCCESS: Imported app package")
    print(f"App location: {app.__file__}")
except ImportError as e:
    print(f"❌ FAILED: Cannot import app package: {e}")
    sys.exit(1)

# Test 2: Check what's in the app package
print(f"\nContents of app package: {dir(app)}")

# Test 3: Try to import create_app directly
try:
    from app import create_app
    print("✅ SUCCESS: Imported create_app directly")
except ImportError as e:
    print(f"❌ FAILED: Cannot import create_app: {e}")

# Test 4: Check individual imports
print("\n=== TESTING INDIVIDUAL IMPORTS ===")
try:
    from app.config import Config
    print("✅ SUCCESS: Imported Config")
except ImportError as e:
    print(f"❌ FAILED: Config import: {e}")

try:
    from app.database.connection import init_database
    print("✅ SUCCESS: Imported init_database")
except ImportError as e:
    print(f"❌ FAILED: init_database import: {e}")

try:
    from app.routes.main import init_main_routes
    print("✅ SUCCESS: Imported init_main_routes")
except ImportError as e:
    print(f"❌ FAILED: init_main_routes import: {e}")

try:
    from app.models.water_quality import WaterQuality
    print("✅ SUCCESS: Imported WaterQuality")
except ImportError as e:
    print(f"❌ FAILED: WaterQuality import: {e}")