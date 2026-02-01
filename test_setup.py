"""
Test script to verify MediaPipe face recognition setup
Run this before starting the main application
"""

import sys

print("🔍 Testing MediaPipe Face Recognition Setup...\n")

# Test 1: Import checks
print("1️⃣ Checking imports...")
try:
    import cv2
    print("   ✅ OpenCV imported successfully")
except ImportError as e:
    print(f"   ❌ OpenCV import failed: {e}")
    sys.exit(1)

try:
    import mediapipe as mp
    print("   ✅ MediaPipe imported successfully")
except ImportError as e:
    print(f"   ❌ MediaPipe import failed: {e}")
    sys.exit(1)

try:
    import numpy as np
    print("   ✅ NumPy imported successfully")
except ImportError as e:
    print(f"   ❌ NumPy import failed: {e}")
    sys.exit(1)

try:
    from sklearn.metrics.pairwise import cosine_similarity
    print("   ✅ Scikit-learn imported successfully")
except ImportError as e:
    print(f"   ❌ Scikit-learn import failed: {e}")
    sys.exit(1)

# Test 2: Face recognizer initialization
print("\n2️⃣ Testing Face Recognizer...")
try:
    from face_utils import FaceRecognizer
    recognizer = FaceRecognizer()
    print("   ✅ FaceRecognizer initialized successfully")
    recognizer.release()
except Exception as e:
    print(f"   ❌ FaceRecognizer initialization failed: {e}")
    sys.exit(1)

# Test 3: Camera test
print("\n3️⃣ Testing camera access...")
try:
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        print("   ✅ Camera accessible")
        cap.release()
    else:
        print("   ⚠️  Camera not accessible (may work in main app)")
except Exception as e:
    print(f"   ⚠️  Camera test failed: {e}")

# Test 4: Flask imports
print("\n4️⃣ Checking Flask dependencies...")
try:
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    from flask_login import LoginManager
    print("   ✅ Flask dependencies imported successfully")
except ImportError as e:
    print(f"   ❌ Flask import failed: {e}")
    sys.exit(1)

print("\n" + "="*50)
print("🎉 All tests passed! Your setup is ready.")
print("="*50)
print("\n📝 Next steps:")
print("   1. Run: python app.py")
print("   2. Open: http://localhost:5000")
print("   3. Register and add students")
print("   4. Test face recognition")
print("\n💡 For deployment, check DEPLOYMENT.md")
