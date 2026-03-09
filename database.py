"""Database operations for face recognition system"""
import sqlite3
import os
from datetime import datetime
from config import DATABASE_PATH, DATABASE_DIR

def initialize_database():
    """Initialize SQLite database with required tables"""
    os.makedirs(DATABASE_DIR, exist_ok=True)
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Create persons table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            email TEXT,
            phone TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create faces table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS faces (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER NOT NULL,
            face_image_path TEXT NOT NULL,
            encoding BLOB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(person_id) REFERENCES persons(id) ON DELETE CASCADE
        )
    ''')
    
    # Create recognition logs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recognition_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            confidence REAL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            source TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id) ON DELETE SET NULL
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✓ Database initialized successfully")

def add_person(name, email=None, phone=None):
    """Add a new person to the database"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO persons (name, email, phone) 
            VALUES (?, ?, ?)
        ''', (name, email, phone))
        conn.commit()
        person_id = cursor.lastrowid
        print(f"✓ Person '{name}' added with ID: {person_id}")
        return person_id
    except sqlite3.IntegrityError:
        print(f"✗ Person '{name}' already exists")
        return None
    finally:
        conn.close()

def add_face(person_id, face_image_path, encoding=None):
    """Add a face record for a person"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO faces (person_id, face_image_path, encoding) 
            VALUES (?, ?, ?)
        ''', (person_id, face_image_path, encoding))
        conn.commit()
        print(f"✓ Face record added for person_id: {person_id}")
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"✗ Error adding face: {e}")
        return None
    finally:
        conn.close()

def get_person_by_id(person_id):
    """Retrieve person details by ID"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, name, email, phone FROM persons WHERE id = ?', (person_id,))
    result = cursor.fetchone()
    conn.close()
    
    return result

def get_person_by_name(name):
    """Retrieve person details by name"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, name, email, phone FROM persons WHERE name = ?', (name,))
    result = cursor.fetchone()
    conn.close()
    
    return result

def get_all_persons():
    """Retrieve all persons from database"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, name, email, phone, created_at FROM persons ORDER BY name')
    results = cursor.fetchall()
    conn.close()
    
    return results

def get_faces_for_person(person_id):
    """Get all face records for a specific person"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, face_image_path, created_at FROM faces 
        WHERE person_id = ? 
        ORDER BY created_at
    ''', (person_id,))
    results = cursor.fetchall()
    conn.close()
    
    return results

def log_recognition(person_id, confidence, source='camera'):
    """Log a successful face recognition event"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO recognition_logs (person_id, confidence, source) 
        VALUES (?, ?, ?)
    ''', (person_id, confidence, source))
    conn.commit()
    conn.close()

def get_recognition_logs(limit=20):
    """Retrieve recent recognition logs"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT p.name, rl.confidence, rl.timestamp, rl.source
        FROM recognition_logs rl
        LEFT JOIN persons p ON rl.person_id = p.id
        ORDER BY rl.timestamp DESC
        LIMIT ?
    ''', (limit,))
    results = cursor.fetchall()
    conn.close()
    
    return results

def delete_person(person_id):
    """Delete a person and all associated face records"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute('DELETE FROM persons WHERE id = ?', (person_id,))
        conn.commit()
        print(f"✓ Person {person_id} deleted successfully")
        return True
    except sqlite3.Error as e:
        print(f"✗ Error deleting person: {e}")
        return False
    finally:
        conn.close()

def get_statistics():
    """Get database statistics"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM persons')
    total_persons = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM faces')
    total_faces = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM recognition_logs')
    total_recognitions = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        'total_persons': total_persons,
        'total_faces': total_faces,
        'total_recognitions': total_recognitions
    }
