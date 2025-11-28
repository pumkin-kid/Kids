"""
PlaySync Flask Application Factory
"""

import os
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

socketio = None

def create_app(config=None):
    """Create and configure Flask application"""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = 'playsync-secret-key-change-in-production'
    if config:
        app.config.update(config)
    
    # Enable CORS
    CORS(app)
    
    # Initialize Socket.IO
    global socketio
    # Use threading async mode for Windows/dev where eventlet may have SSL issues.
    # Allow override via ASYNC_MODE env var so production can use eventlet if available.
    async_mode = os.environ.get('ASYNC_MODE', 'threading')
    socketio = SocketIO(
        app,
        cors_allowed_origins="*",
        ping_timeout=60,
        ping_interval=25,
        async_mode=async_mode,
    )
    
    # Register blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    # Register Socket.IO events
    from app import socketio_events
    
    return app, socketio
