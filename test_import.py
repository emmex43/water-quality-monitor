import sys
print("Python path:")
for path in sys.path:
    print(path)

print("\nTrying to import app...")
try:
    from app import create_app
    print("✅ SUCCESS: Import worked!")
except ImportError as e:
    print(f"❌ FAILED: {e}")