"""Face Recognition System - Flask Web Application"""
from flask import Flask, render_template, jsonify, request, send_from_directory
import os
from database import (
    initialize_database, add_person, get_person_by_name, get_person_by_id,
    get_all_persons, get_faces_for_person, get_recognition_logs,
    delete_person, get_statistics
)
from config import REGISTERED_FACES_DIR

app = Flask(__name__)

# Initialize database on startup
initialize_database()

# ==================== Page Routes ====================

@app.route('/')
def dashboard():
    """Dashboard page"""
    return render_template('dashboard.html')

@app.route('/persons')
def persons_page():
    """Persons management page"""
    return render_template('persons.html')

@app.route('/logs')
def logs_page():
    """Recognition logs page"""
    return render_template('logs.html')

# ==================== API Routes ====================

@app.route('/api/stats')
def api_stats():
    """Get system statistics"""
    stats = get_statistics()
    return jsonify(stats)

@app.route('/api/persons', methods=['GET'])
def api_get_persons():
    """Get all persons"""
    persons = get_all_persons()
    result = []
    for p in persons:
        person_id, name, email, phone, created_at = p
        faces = get_faces_for_person(person_id)
        result.append({
            'id': person_id,
            'name': name,
            'email': email or '',
            'phone': phone or '',
            'created_at': created_at,
            'face_count': len(faces)
        })
    return jsonify(result)

@app.route('/api/persons', methods=['POST'])
def api_add_person():
    """Add a new person"""
    data = request.get_json()
    name = data.get('name', '').strip()
    email = data.get('email', '').strip() or None
    phone = data.get('phone', '').strip() or None

    if not name:
        return jsonify({'error': 'Name is required'}), 400

    person_id = add_person(name, email, phone)
    if person_id:
        return jsonify({'id': person_id, 'name': name, 'message': f"Person '{name}' added successfully"}), 201
    else:
        return jsonify({'error': f"Person '{name}' already exists"}), 409

@app.route('/api/persons/<int:person_id>', methods=['GET'])
def api_get_person(person_id):
    """Get a specific person with their faces"""
    person = get_person_by_id(person_id)
    if not person:
        return jsonify({'error': 'Person not found'}), 404

    pid, name, email, phone = person
    faces = get_faces_for_person(pid)
    face_list = []
    for face_id, face_path, created_at in faces:
        # Extract relative path for serving
        face_list.append({
            'id': face_id,
            'path': face_path,
            'created_at': created_at
        })

    return jsonify({
        'id': pid,
        'name': name,
        'email': email or '',
        'phone': phone or '',
        'faces': face_list,
        'face_count': len(face_list)
    })

@app.route('/api/persons/<int:person_id>', methods=['DELETE'])
def api_delete_person(person_id):
    """Delete a person"""
    person = get_person_by_id(person_id)
    if not person:
        return jsonify({'error': 'Person not found'}), 404

    success = delete_person(person_id)
    if success:
        return jsonify({'message': f"Person '{person[1]}' deleted successfully"})
    else:
        return jsonify({'error': 'Failed to delete person'}), 500

@app.route('/api/logs')
def api_get_logs():
    """Get recognition logs"""
    limit = request.args.get('limit', 50, type=int)
    logs = get_recognition_logs(limit)
    result = []
    for name, confidence, timestamp, source in logs:
        result.append({
            'name': name or 'Unknown',
            'confidence': round(confidence, 4) if confidence else 0,
            'timestamp': timestamp,
            'source': source
        })
    return jsonify(result)

@app.route('/faces/<path:filepath>')
def serve_face_image(filepath):
    """Serve face images from the registered_faces directory"""
    return send_from_directory(REGISTERED_FACES_DIR, filepath)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
