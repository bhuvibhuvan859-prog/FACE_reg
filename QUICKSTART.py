#!/usr/bin/env python
# QUICK START GUIDE FOR FACE RECOGNITION PROJECT

"""
╔════════════════════════════════════════════════════════════════════════════╗
║           FACE RECOGNITION WITH DATA RETRIEVAL - QUICK START              ║
╚════════════════════════════════════════════════════════════════════════════╝

STEP 1: Install Dependencies
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
$ pip install -r requirements.txt

Verify installation:
$ python setup_check.py

STEP 2: Initialize Database
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
$ python main.py init-db

STEP 3: Register People
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
First, add a person to the system:
$ python main.py add-person-cmd --name "John Doe" --email "john@example.com"

Then register their face using camera (capture 5 face samples):
$ python main.py register-faces --name "John Doe" --count 5

Camera Controls:
  • Position face in front of the camera
  • Press SPACE to capture each face sample
  • Press ESC to cancel

STEP 4: Test Face Recognition
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Start real-time recognition:
$ python main.py recognize-from-camera

Camera Controls:
  • Press 'q' to quit
  • Recognized faces will appear in the feed with names

STEP 5: View Results
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Check recognition statistics:
$ python main.py statistics

View recognition history:
$ python main.py view-logs --limit 20

List all registered people:
$ python main.py list-persons

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

COMMON COMMANDS REFERENCE:

Person Management:
  python main.py add-person-cmd --name "Name"
  python main.py list-persons
  python main.py view-person --name "Name"
  python main.py delete-person-cmd --name "Name"

Face Registration & Recognition:
  python main.py register-faces --name "Name" --count 5
  python main.py recognize-from-camera
  python main.py recognize-from-image --image "path/to/image.jpg"

Logs & Stats:
  python main.py view-logs --limit 20
  python main.py statistics

Database:
  python main.py init-db

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PROJECT STRUCTURE:

FACE_reg/
├── main.py                      ← Run all commands from here
├── config.py                    ← Customize settings (camera, detection, etc)
├── database.py                  ← Database operations
├── face_recognition_module.py   ← Face detection & recognition logic
├── setup_check.py               ← Verify installation
├── example.py                   ← See example usage
├── ADVANCED_USAGE.md            ← Advanced topics
├── README.md                    ← Full documentation
├── requirements.txt             ← Python dependencies
├── data/
│   └── registered_faces/        ← Face images stored here
├── database/
│   └── faces.db                 ← SQLite database
└── logs/                        ← Application logs

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TIPS FOR BETTER ACCURACY:

✓ Register 8-10 face samples per person (minimum 5)
✓ Vary angles: face forward, left, right, up, down
✓ Vary lighting: bright light, dim light, side light
✓ Use different expressions: neutral, smile, serious
✓ Keep good distance (50-100cm from camera)
✓ Ensure face is clearly visible

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NEED HELP?

1. Check README.md for detailed documentation
2. Run: python setup_check.py
3. See example usage in example.py
4. Check ADVANCED_USAGE.md for advanced topics

Happy recognizing! 🎉

"""
