"""Configuration settings for Face Recognition project"""
import os
import cv2

# Project paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
REGISTERED_FACES_DIR = os.path.join(DATA_DIR, 'registered_faces')
DATABASE_DIR = os.path.join(BASE_DIR, 'database')
LOGS_DIR = os.path.join(BASE_DIR, 'logs')

# Database
DATABASE_PATH = os.path.join(DATABASE_DIR, 'faces.db')

# Face Recognition settings
CASCADE_PATH = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
CONFIDENCE_THRESHOLD = 0.6
MIN_FACE_SIZE = (50, 50)

# Camera settings
CAMERA_INDEX = 0
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
FPS = 30

# Encoding settings
FACE_ENCODING_SIZE = 128
