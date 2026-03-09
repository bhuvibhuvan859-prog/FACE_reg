# Face Recognition with Data Retrieval

A Python-based face recognition system that combines OpenCV for face detection/recognition with SQLite for data management. This project enables you to register, recognize, and manage face data efficiently.

## 🎯 Features

- **Face Detection & Recognition** - Uses OpenCV Cascade Classifiers and LBPH algorithm
- **SQLite Data Management** - Store persons, faces, and recognition logs
- **Real-time Recognition** - Live camera feed recognition
- **Image Recognition** - Recognize faces in static images
- **Person Management** - Add, view, list, and delete persons
- **Face Registration** - Capture multiple face samples per person
- **Recognition Logs** - Track all recognition events with confidence scores
- **Statistics Dashboard** - View system statistics

## 📁 Project Structure

```
FACE_reg/
├── main.py                      # CLI application entry point
├── config.py                    # Configuration settings
├── database.py                  # SQLite database operations
├── face_recognition_module.py   # Face recognition logic
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── data/
│   └── registered_faces/        # Stores face images organized by person
├── database/
│   └── faces.db                 # SQLite database file
└── logs/                        # Application logs
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Initialize Database

```bash
python main.py init-db
```

### 3. Register a Person with Faces

```bash
python main.py register-faces --name "John Doe" --count 5
```

- A camera window will open
- Position your face in front of the camera
- Press **SPACE** to capture each face
- Press **ESC** to cancel
- The system will capture 5 face samples

### 4. Recognize Faces in Real-time

```bash
python main.py recognize-from-camera
```

- The camera feed will open
- Registered faces will be identified
- Press **q** to quit

## 📋 Available Commands

### Person Management

```bash
# Add a new person
python main.py add-person-cmd --name "Jane Doe" --email "jane@example.com" --phone "1234567890"

# List all registered persons
python main.py list-persons

# View details of a specific person
python main.py view-person --name "John Doe"

# Delete a person
python main.py delete-person-cmd --name "John Doe"
```

### Face Recognition

```bash
# Real-time recognition from camera
python main.py recognize-from-camera

# Recognize faces in an image file
python main.py recognize-from-image --image "path/to/image.jpg"
```

### Face Registration

```bash
# Register faces for a person (with camera)
python main.py register-faces --name "Person Name" --count 5
```

### Logs & Statistics

```bash
# View recent recognition logs
python main.py view-logs --limit 20

# Display system statistics
python main.py statistics
```

### Database

```bash
# Initialize/reset database
python main.py init-db
```

## 🗄️ Database Schema

### persons
- `id` - Person ID (Primary Key)
- `name` - Person's name (Unique)
- `email` - Contact email
- `phone` - Contact phone
- `created_at` - Registration timestamp

### faces
- `id` - Face record ID (Primary Key)
- `person_id` - Reference to persons (Foreign Key)
- `face_image_path` - Path to face image file
- `encoding` - Face encoding (for future use with advanced algorithms)
- `created_at` - Timestamp

### recognition_logs
- `id` - Log ID (Primary Key)
- `person_id` - Recognized person ID
- `confidence` - Recognition confidence score (0-1)
- `timestamp` - Recognition event time
- `source` - Source (camera/image file)

## ⚙️ Configuration

Edit `config.py` to customize:

```python
# Camera settings
CAMERA_INDEX = 0              # Camera device index
FRAME_WIDTH = 640             # Frame width
FRAME_HEIGHT = 480            # Frame height

# Face Recognition
MIN_FACE_SIZE = (50, 50)      # Minimum face dimensions
CONFIDENCE_THRESHOLD = 0.6    # Recognition confidence threshold
```

## 📊 How It Works

### Face Detection
- Uses Haar Cascade Classifier (pre-trained OpenCV model)
- Detects faces in real-time with configurable sensitivity

### Face Recognition
- Uses LBPH (Local Binary Patterns Histograms) algorithm
- Trains on registered face images
- Compares detected faces against training data
- Returns person name and confidence score

### Data Storage
- Organizes face images: `data/registered_faces/{person_name}/{image}.jpg`
- Stores metadata in SQLite for quick retrieval
- Maintains recognition history with timestamps and confidence

## 🔧 Requirements

- Python 3.7+
- OpenCV 4.8.1
- NumPy 1.24.3
- Pillow 10.0.0
- Click 8.1.7

## 📝 Example Usage Workflow

```bash
# 1. Initialize system
python main.py init-db

# 2. Add a new person
python main.py add-person-cmd --name "Alice"

# 3. Register their face samples
python main.py register-faces --name "Alice" --count 5

# 4. View registered person
python main.py view-person --name "Alice"

# 5. Start recognition
python main.py recognize-from-camera

# 6. Check statistics
python main.py statistics

# 7. View recognition logs
python main.py view-logs --limit 10
```

## 🎓 Use Cases

1. **Access Control** - Identify employees/members
2. **Attendance System** - Automated attendance tracking
3. **Security Monitoring** - Detect and track persons of interest
4. **Retail Analytics** - Customer identification and behavior analysis
5. **Photo Organization** - Automatic photo grouping by person

## ⚠️ Limitations & Future Improvements

### Current Limitations
- LBPH algorithm requires sufficient lighting
- Performance reduces with large databases (1000+ persons)
- Single-face detection per frame

### Future Enhancements
- [ ] Deep learning models (ResNet, VGGFace)
- [ ] Multiple face detection per frame
- [ ] GPU acceleration support
- [ ] Web interface (Flask)
- [ ] Multi-camera support
- [ ] Face encoding storage for faster recognition
- [ ] REST API endpoints
- [ ] Advanced filtering and search

## 🐛 Troubleshooting

### No faces detected
- Ensure good lighting conditions
- Position face directly facing camera
- Adjust `MIN_FACE_SIZE` in config.py

### Low recognition accuracy
- Register more face samples (8-10 per person)
- Vary angles and lighting during registration
- Lower `CONFIDENCE_THRESHOLD` for more lenient matching

### Camera not working
- Change `CAMERA_INDEX` in config.py
- Ensure webcam is not used by another application
- Check camera permissions

## 📄 License

This project is created for educational and practical purposes.

## 👨‍💻 Author

Created as a face recognition system with SQLite data management.

---

**Happy recognizing! 🎉**