"""Face recognition module using OpenCV"""
import cv2
import numpy as np
import os
from config import CASCADE_PATH, MIN_FACE_SIZE, CONFIDENCE_THRESHOLD, REGISTERED_FACES_DIR
from database import log_recognition

class FaceRecognizer:
    """Face recognition system using OpenCV"""
    
    def __init__(self):
        """Initialize face recognizer with cascade classifier"""
        self.cascade = cv2.CascadeClassifier(CASCADE_PATH)
        self.face_recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.labels_dict = {}
        self.reverse_labels_dict = {}
        self.label_counter = 0
        self.trained = False
        
    def detect_faces(self, image):
        """Detect faces in an image"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.cascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=5,
            minSize=MIN_FACE_SIZE
        )
        return faces
    
    def save_face_image(self, image, person_name):
        """Save a face image for a person"""
        person_dir = os.path.join(REGISTERED_FACES_DIR, person_name)
        os.makedirs(person_dir, exist_ok=True)
        
        # Generate filename based on timestamp
        existing_files = len(os.listdir(person_dir))
        filename = f"{person_name}_{existing_files + 1}.jpg"
        filepath = os.path.join(person_dir, filename)
        
        cv2.imwrite(filepath, image)
        print(f"✓ Face image saved: {filepath}")
        return filepath
    
    def train_recognizer(self, person_faces_dict):
        """Train the face recognizer with labeled faces"""
        if not person_faces_dict:
            print("✗ No training data available")
            return False
        
        faces = []
        labels = []
        self.labels_dict = {}
        self.reverse_labels_dict = {}
        self.label_counter = 0
        
        for person_name, face_images in person_faces_dict.items():
            label = self.label_counter
            self.labels_dict[person_name] = label
            self.reverse_labels_dict[label] = person_name
            self.label_counter += 1
            
            for face_image in face_images:
                gray = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
                faces.append(gray)
                labels.append(label)
        
        if faces:
            self.face_recognizer.train(faces, np.array(labels))
            self.trained = True
            print(f"✓ Recognizer trained with {len(self.labels_dict)} persons")
            return True
        return False
    
    def recognize_face(self, face_image):
        """Recognize a face and return person name and confidence"""
        if not self.trained:
            return None, None
        
        gray = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
        label, confidence = self.face_recognizer.predict(gray)
        
        if confidence < CONFIDENCE_THRESHOLD:
            person_name = self.reverse_labels_dict.get(label, "Unknown")
            return person_name, confidence
        
        return "Unknown", confidence
    
    def draw_face_box(self, image, faces, recognize=False):
        """Draw rectangles around detected faces"""
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            if recognize:
                face_roi = image[y:y+h, x:x+w]
                person_name, confidence = self.recognize_face(face_roi)
                
                label = f"{person_name} ({confidence:.2f})" if person_name != "Unknown" else person_name
                cv2.putText(image, label, (x, y - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        return image

def load_training_data(registered_faces_dir):
    """Load training data from registered faces directory"""
    person_faces = {}
    
    if not os.path.exists(registered_faces_dir):
        print(f"✗ Directory not found: {registered_faces_dir}")
        return person_faces
    
    for person_name in os.listdir(registered_faces_dir):
        person_dir = os.path.join(registered_faces_dir, person_name)
        
        if not os.path.isdir(person_dir):
            continue
        
        faces = []
        for img_file in os.listdir(person_dir):
            if img_file.lower().endswith(('.jpg', '.jpeg', '.png')):
                img_path = os.path.join(person_dir, img_file)
                image = cv2.imread(img_path)
                
                if image is not None:
                    faces.append(image)
        
        if faces:
            person_faces[person_name] = faces
            print(f"✓ Loaded {len(faces)} faces for {person_name}")
    
    return person_faces
