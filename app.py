"""
Simple Flask Backend for Finger Counter
- No camera required (processes frames from frontend)
- Lightweight and cloud-friendly
- Works on Railway, Render, Heroku
"""

import os
import sys
import json
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

app = Flask(__name__, template_folder='templates')
CORS(app)

# Simple game state
game_state = {
    'status': 'ready'
}

@app.route('/', methods=['GET'])
def index():
    """Serve the main game page"""
    return render_template('index.html')

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'finger-counter-backend',
        'version': '1.0.0'
    }), 200

@app.route('/api/status', methods=['GET'])
def status():
    """Get current game status"""
    return jsonify({
        'game_status': game_state['status'],
        'ready': True
    }), 200

@app.route('/api/process-frame', methods=['POST'])
def process_frame():
    """
    Process frame from frontend
    
    Expected POST data:
    {
        'frameData': base64_encoded_image,
        'width': number,
        'height': number
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'frameData' not in data:
            return jsonify({'error': 'No frame data provided'}), 400
        
        # For now, return dummy data
        # The frontend handles MediaPipe processing
        return jsonify({
            'finger_count': 0,
            'extended_fingers': [],
            'palm_facing': False,
            'success': True
        }), 200
        
    except Exception as e:
        print(f"Error processing frame: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/favicon.ico')
def favicon():
    """Return a simple favicon to suppress 404"""
    return '', 204

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Get port from environment or use default
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    print(f"Starting Finger Counter Backend on port {port}...")
    print(f"Debug mode: {debug}")
    print(f"CORS enabled for all origins")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug,
        use_reloader=False
    )
