"""
PlaySync Routes
Web UI endpoints for landing and room pages
"""

from flask import Blueprint, render_template, request, jsonify
from app.room_manager import room_manager
from app.utils import generate_qr_code, generate_display_name, get_random_avatar_color

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Landing page"""
    return render_template('index.html')

@main_bp.route('/room/<room_id>')
def room(room_id):
    """Room page"""
    room_obj = room_manager.get_room(room_id)
    
    if not room_obj:
        return render_template('room_not_found.html', room_id=room_id), 404
    
    if room_obj.is_expired():
        return render_template('room_expired.html', room_id=room_id), 410
    
    # Generate QR code for this room
    full_url = request.base_url  # e.g., http://localhost:5000/room/ABC123
    qr_code_b64 = generate_qr_code(full_url)
    
    return render_template(
        'room.html',
        room_id=room_id,
        qr_code=qr_code_b64,
        max_players=room_obj.max_players,
        current_players=room_obj.get_player_count()
    )

@main_bp.route('/api/room/<room_id>')
def get_room_info(room_id):
    """API: Get room information"""
    room_info = room_manager.get_room_info(room_id)
    
    if not room_info:
        return jsonify({'error': 'Room not found'}), 404
    
    return jsonify(room_info)

@main_bp.route('/api/create-room', methods=['POST'])
def create_room_api():
    """API: Create a new room"""
    room_id = room_manager.create_room()
    return jsonify({
        'room_id': room_id,
        'room_url': f'/room/{room_id}'
    })
