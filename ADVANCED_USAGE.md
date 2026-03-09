"""
Advanced Configuration and Usage Examples
Customize the system for your specific needs
"""

# ==================== CONFIG CUSTOMIZATION ====================

# To customize settings, edit config.py:

"""
# config.py - Example customizations

# 1. CAMERA SETTINGS
CAMERA_INDEX = 0              # Use 0 for default camera, 1 for second camera
FRAME_WIDTH = 1280            # Increase for better quality (1280, 1920, etc)
FRAME_HEIGHT = 720            # Match the width/height ratio
FPS = 30                       # Frames per second

# 2. FACE DETECTION TUNING
MIN_FACE_SIZE = (40, 40)      # Smaller = detect smaller faces (but slower)
MIN_FACE_SIZE = (80, 80)      # Larger = faster but misses small faces

# 3. RECOGNITION SENSITIVITY
CONFIDENCE_THRESHOLD = 0.4    # Lower = more lenient (0-1 scale)
CONFIDENCE_THRESHOLD = 0.8    # Higher = more strict
"""

# ==================== ADVANCED USAGE ====================

"""
1. BATCH REGISTRATION - Register multiple people programmatically:

    from database import initialize_database, add_person
    initialize_database()
    
    people = [
        ("Person 1", "email1@company.com", "555-1001"),
        ("Person 2", "email2@company.com", "555-1002"),
        ("Person 3", "email3@company.com", "555-1003"),
    ]
    
    for name, email, phone in people:
        add_person(name, email, phone)

2. BATCH FACE RECOGNITION - Process multiple images:

    import cv2
    from face_recognition_module import FaceRecognizer, load_training_data
    from config import REGISTERED_FACES_DIR
    import glob
    
    recognizer = FaceRecognizer()
    person_faces = load_training_data(REGISTERED_FACES_DIR)
    recognizer.train_recognizer(person_faces)
    
    for image_path in glob.glob('test_images/*.jpg'):
        image = cv2.imread(image_path)
        faces = recognizer.detect_faces(image)
        image = recognizer.draw_face_box(image, faces, recognize=True)
        cv2.imwrite(f'results/{image_path.split("/")[-1]}', image)

3. DATABASE QUERIES - Direct database access:

    from database import get_all_persons, get_faces_for_person, get_recognition_logs
    
    # Get all persons
    for person_id, name, email, phone, created_at in get_all_persons():
        print(f"{name}: {email}")
    
    # Get specific person's faces
    faces = get_faces_for_person(person_id=1)
    for face_id, path, created_at in faces:
        print(f"Face: {path}")
    
    # View recognition history
    for name, confidence, timestamp, source in get_recognition_logs(limit=50):
        print(f"{name}: {confidence:.2f} at {timestamp}")

4. VIDEO PROCESSING - Process video files:

    import cv2
    from face_recognition_module import FaceRecognizer, load_training_data
    from config import REGISTERED_FACES_DIR
    
    recognizer = FaceRecognizer()
    person_faces = load_training_data(REGISTERED_FACES_DIR)
    recognizer.train_recognizer(person_faces)
    
    cap = cv2.VideoCapture('video_file.mp4')
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('output.mp4', fourcc, 30, (int(cap.get(3)), int(cap.get(4))))
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        faces = recognizer.detect_faces(frame)
        frame = recognizer.draw_face_box(frame, faces, recognize=True)
        out.write(frame)
    
    cap.release()
    out.release()

5. CUSTOM FACE DETECTION - Process only high-confidence detections:

    from face_recognition_module import FaceRecognizer
    
    recognizer = FaceRecognizer()
    faces = recognizer.detect_faces(image)
    
    # Filter by size
    min_size = 50
    filtered_faces = [f for f in faces if f[2] > min_size and f[3] > min_size]
    
    # Process only the largest face
    if filtered_faces:
        largest = max(filtered_faces, key=lambda x: x[2] * x[3])
        person_name, confidence = recognizer.recognize_face(image[largest[1]:largest[1]+largest[3], largest[0]:largest[0]+largest[2]])
"""

# ==================== PERFORMANCE TIPS ====================

"""
IMPROVE RECOGNITION SPEED:
- Reduce frame size (640x480 instead of 1920x1080)
- Increase MIN_FACE_SIZE to skip small/distant faces
- Use GPU acceleration (requires CUDA and OpenCV built with CUDA)
- Implement face detection caching

IMPROVE RECOGNITION ACCURACY:
- Register 8-10 face samples per person (5 is minimum)
- Include varied angles, lighting, and expressions
- Keep faces well-lit during both registration and recognition
- Remove very similar duplicate faces from registration set
- Lower CONFIDENCE_THRESHOLD if false negatives are high
- Raise CONFIDENCE_THRESHOLD if false positives are high

OPTIMIZE DATABASE:
- Regularly backup database/faces.db
- Clean up old recognition logs: DELETE FROM recognition_logs WHERE timestamp < datetime('now', '-90 days')
- Index frequently queried columns in the database
"""

# ==================== TROUBLESHOOTING ====================

"""
ISSUE: "cv2.error: (-2:Unspecified error)"
FIX: Reinstall OpenCV with: pip install --upgrade opencv-python

ISSUE: "No camera detected"
FIX: Check CAMERA_INDEX in config.py, try 0, 1, or 2

ISSUE: "Poor recognition accuracy"
FIX: Register more samples, improve lighting, adjust CONFIDENCE_THRESHOLD

ISSUE: "SQLite database locked"
FIX: Only one process should write to database, restart application

ISSUE: "Face detection very slow"
FIX: Reduce frame size, increase MIN_FACE_SIZE in config.py
"""

print(__doc__)
