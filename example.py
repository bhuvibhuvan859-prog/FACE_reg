"""
Example usage of the Face Recognition System
Demonstrates common operations
"""

from database import initialize_database, add_person, get_all_persons, get_statistics
from face_recognition_module import load_training_data
import sys

def main():
    print("="*70)
    print("Face Recognition System - Quick Demo")
    print("="*70)
    
    # Initialize database
    print("\n[1/5] Initializing database...")
    initialize_database()
    
    # Add sample persons
    print("\n[2/5] Adding sample persons...")
    persons = [
        ("Alice Johnson", "alice@example.com", "555-1001"),
        ("Bob Smith", "bob@example.com", "555-1002"),
        ("Carol White", "carol@example.com", "555-1003"),
    ]
    
    for name, email, phone in persons:
        add_person(name, email, phone)
    
    # List all persons
    print("\n[3/5] Listing all registered persons...")
    all_persons = get_all_persons()
    for person in all_persons:
        print(f"  - {person[1]} ({person[2]}, {person[3]})")
    
    # Load training data
    print("\n[4/5] Loading training data from registered faces...")
    from config import REGISTERED_FACES_DIR
    person_faces = load_training_data(REGISTERED_FACES_DIR)
    print(f"  Loaded faces for: {len(person_faces)} persons")
    
    # Display statistics
    print("\n[5/5] System Statistics:")
    stats = get_statistics()
    print(f"  Total Persons: {stats['total_persons']}")
    print(f"  Total Face Images: {stats['total_faces']}")
    print(f"  Total Recognition Events: {stats['total_recognitions']}")
    
    print("\n" + "="*70)
    print("✓ Demo Complete!")
    print("\nNext Steps:")
    print("  1. Register faces: python main.py register-faces --name 'Your Name'")
    print("  2. Start recognition: python main.py recognize-from-camera")
    print("  3. View statistics: python main.py statistics")
    print("="*70)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)
