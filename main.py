"""Face Recognition with Data Retrieval - Main CLI Application"""
import click
import cv2
import os
from database import (
    initialize_database, add_person, add_face, get_person_by_name,
    get_all_persons, get_faces_for_person, get_recognition_logs,
    delete_person, get_statistics, log_recognition
)
from face_recognition_module import FaceRecognizer, load_training_data
from config import REGISTERED_FACES_DIR, CAMERA_INDEX, FRAME_WIDTH, FRAME_HEIGHT

@click.group()
def cli():
    """Face Recognition System with Data Retrieval"""
    pass

# ==================== Person Management ====================

@cli.command()
@click.option('--name', prompt='Enter person name', help='Name of the person')
@click.option('--email', default='', help='Email address')
@click.option('--phone', default='', help='Phone number')
def add_person_cmd(name, email, phone):
    """Add a new person to the database"""
    initialize_database()
    add_person(name, email if email else None, phone if phone else None)

@cli.command()
def list_persons():
    """List all registered persons"""
    initialize_database()
    persons = get_all_persons()
    
    if not persons:
        click.echo("No persons registered yet.")
        return
    
    click.echo("\n" + "="*70)
    click.echo(f"{'ID':<5} {'Name':<20} {'Email':<25} {'Phone':<15}")
    click.echo("="*70)
    
    for person in persons:
        person_id, name, email, phone, created_at = person
        email = email or '-'
        phone = phone or '-'
        click.echo(f"{person_id:<5} {name:<20} {email:<25} {phone:<15}")
    
    click.echo("="*70)

@cli.command()
@click.option('--name', prompt='Enter person name', help='Name of the person to delete')
def delete_person_cmd(name):
    """Delete a person from database"""
    initialize_database()
    person = get_person_by_name(name)
    
    if not person:
        click.echo(f"✗ Person '{name}' not found")
        return
    
    if click.confirm(f"Delete '{name}' and all associated faces?"):
        delete_person(person[0])

@cli.command()
@click.option('--name', prompt='Enter person name', help='Name of the person')
def view_person(name):
    """View details of a specific person"""
    initialize_database()
    person = get_person_by_name(name)
    
    if not person:
        click.echo(f"✗ Person '{name}' not found")
        return
    
    person_id, name, email, phone = person
    click.echo(f"\nPerson Details:")
    click.echo(f"  ID: {person_id}")
    click.echo(f"  Name: {name}")
    click.echo(f"  Email: {email or '-'}")
    click.echo(f"  Phone: {phone or '-'}\n")
    
    faces = get_faces_for_person(person_id)
    click.echo(f"Registered Faces: {len(faces)}")
    for face_id, face_path, created_at in faces:
        click.echo(f"  - {face_path} ({created_at})")

# ==================== Face Registration ====================

@cli.command()
@click.option('--name', prompt='Enter person name', help='Name of the person')
@click.option('--count', default=5, help='Number of face samples to capture')
def register_faces(name, count):
    """Register faces for a person using camera"""
    initialize_database()
    
    # Add person if not exists
    person = get_person_by_name(name)
    if not person:
        person_id = add_person(name)
    else:
        person_id = person[0]
    
    if not person_id:
        click.echo(f"✗ Could not register person: {name}")
        return
    
    click.echo(f"\nStarting face registration for: {name}")
    click.echo(f"Press SPACE to capture | ESC to cancel")
    
    recognizer = FaceRecognizer()
    cap = cv2.VideoCapture(CAMERA_INDEX)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
    
    captured_count = 0
    
    try:
        while captured_count < count:
            ret, frame = cap.read()
            if not ret:
                click.echo("✗ Failed to read frame")
                break
            
            faces = recognizer.detect_faces(frame)
            
            if len(faces) > 0:
                frame = recognizer.draw_face_box(frame, faces)
                cv2.putText(frame, f"Captured: {captured_count}/{count}", 
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                cv2.putText(frame, "No face detected", 
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
            cv2.imshow(f'Register Faces - {name}', frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC
                break
            elif key == 32 and len(faces) > 0:  # SPACE
                face_roi = frame[faces[0][1]:faces[0][1]+faces[0][3], 
                                faces[0][0]:faces[0][0]+faces[0][2]]
                filepath = recognizer.save_face_image(face_roi, name)
                add_face(person_id, filepath)
                captured_count += 1
                click.echo(f"✓ Face {captured_count}/{count} captured")
    
    finally:
        cap.release()
        cv2.destroyAllWindows()
        click.echo(f"✓ Registration complete: {captured_count} faces captured")

# ==================== Face Recognition ====================

@cli.command()
def recognize_from_camera():
    """Recognize faces in real-time from camera"""
    initialize_database()
    
    click.echo("Loading training data...")
    person_faces = load_training_data(REGISTERED_FACES_DIR)
    
    if not person_faces:
        click.echo("✗ No registered faces found. Please register faces first.")
        return
    
    recognizer = FaceRecognizer()
    recognizer.train_recognizer(person_faces)
    
    click.echo("Starting face recognition (Press 'q' to quit)...")
    cap = cv2.VideoCapture(CAMERA_INDEX)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            faces = recognizer.detect_faces(frame)
            frame = recognizer.draw_face_box(frame, faces, recognize=True)
            
            cv2.imshow('Face Recognition', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    finally:
        cap.release()
        cv2.destroyAllWindows()

@cli.command()
@click.option('--image', prompt='Enter image path', help='Path to image file')
def recognize_from_image(image):
    """Recognize faces in a static image"""
    initialize_database()
    
    if not os.path.exists(image):
        click.echo(f"✗ Image not found: {image}")
        return
    
    click.echo("Loading training data...")
    person_faces = load_training_data(REGISTERED_FACES_DIR)
    
    if not person_faces:
        click.echo("✗ No registered faces found")
        return
    
    recognizer = FaceRecognizer()
    recognizer.train_recognizer(person_faces)
    
    frame = cv2.imread(image)
    faces = recognizer.detect_faces(frame)
    
    if not faces:
        click.echo("✗ No faces detected in image")
    else:
        frame = recognizer.draw_face_box(frame, faces, recognize=True)
        output_path = image.replace('.jpg', '_recognized.jpg').replace('.png', '_recognized.png')
        cv2.imwrite(output_path, frame)
        click.echo(f"✓ Recognized image saved: {output_path}")

# ==================== Logs & Statistics ====================

@cli.command()
@click.option('--limit', default=10, help='Number of recent logs to display')
def view_logs(limit):
    """View recognition logs"""
    initialize_database()
    logs = get_recognition_logs(limit)
    
    if not logs:
        click.echo("No recognition logs available.")
        return
    
    click.echo("\n" + "="*70)
    click.echo(f"{'Name':<20} {'Confidence':<15} {'Timestamp':<25} {'Source':<10}")
    click.echo("="*70)
    
    for name, confidence, timestamp, source in logs:
        name = name or 'Unknown'
        click.echo(f"{name:<20} {confidence:<15.2f} {timestamp:<25} {source:<10}")
    
    click.echo("="*70)

@cli.command()
def statistics():
    """Display system statistics"""
    initialize_database()
    stats = get_statistics()
    
    click.echo("\n" + "="*50)
    click.echo("Face Recognition System Statistics")
    click.echo("="*50)
    click.echo(f"Total Persons Registered: {stats['total_persons']}")
    click.echo(f"Total Face Images: {stats['total_faces']}")
    click.echo(f"Total Recognition Events: {stats['total_recognitions']}")
    click.echo("="*50)

# ==================== Database Management ====================

@cli.command()
def init_db():
    """Initialize the database"""
    initialize_database()
    click.echo("✓ Database initialized")

if __name__ == '__main__':
    cli()
