"""
Setup and validation script for Face Recognition project
Run this to verify all dependencies are installed correctly
"""

import sys
import subprocess

def check_python_version():
    """Check if Python version is 3.7+"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print(f"✗ Python 3.7+ required. You have {version.major}.{version.minor}")
        return False
    print(f"✓ Python version: {version.major}.{version.minor}.{version.micro}")
    return True

def check_dependencies():
    """Check if all required packages are installed"""
    required = {
        'cv2': 'opencv-python',
        'numpy': 'numpy',
        'PIL': 'Pillow',
        'click': 'click'
    }
    
    missing = []
    for module, package_name in required.items():
        try:
            __import__(module)
            print(f"✓ {package_name} installed")
        except ImportError:
            print(f"✗ {package_name} NOT installed")
            missing.append(package_name)
    
    if missing:
        print(f"\nInstall missing packages with:")
        print(f"  pip install {' '.join(missing)}")
        return False
    return True

def check_camera():
    """Check if camera is accessible"""
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            ret, frame = cap.read()
            cap.release()
            if ret:
                print("✓ Camera is accessible")
                return True
        print("✗ Camera not accessible or not found")
        return False
    except Exception as e:
        print(f"✗ Camera check failed: {e}")
        return False

def check_directories():
    """Check if required directories exist"""
    import os
    dirs = [
        'data',
        'data/registered_faces',
        'database',
        'logs'
    ]
    
    for dir_path in dirs:
        if os.path.exists(dir_path):
            print(f"✓ Directory exists: {dir_path}")
        else:
            print(f"! Directory not found (will be created): {dir_path}")
    
    return True

def main():
    print("="*70)
    print("Face Recognition System - Setup Verification")
    print("="*70)
    
    print("\n[1/4] Checking Python version...")
    python_ok = check_python_version()
    
    print("\n[2/4] Checking dependencies...")
    deps_ok = check_dependencies()
    
    print("\n[3/4] Checking camera...")
    camera_ok = check_camera()
    
    print("\n[4/4] Checking directories...")
    dirs_ok = check_directories()
    
    print("\n" + "="*70)
    if python_ok and deps_ok:
        print("✓ Setup is ready!")
        if not camera_ok:
            print("⚠ Camera not detected (not required for static image recognition)")
        print("\nTo get started:")
        print("  1. python main.py init-db")
        print("  2. python main.py register-faces --name 'Your Name'")
        print("  3. python main.py recognize-from-camera")
    else:
        print("✗ Setup incomplete. Please install missing dependencies.")
        print("  pip install -r requirements.txt")
    print("="*70)

if __name__ == "__main__":
    main()
