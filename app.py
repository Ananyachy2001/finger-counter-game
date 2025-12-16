import cv2
import mediapipe as mp
import numpy as np
import math
import base64
import traceback
import sys
from io import BytesIO
from flask import Flask, render_template, Response, jsonify, send_file
from flask_cors import CORS
import threading
import time

app = Flask(__name__)
CORS(app)

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_drawing = mp.solutions.drawing_utils

# Game state (shared across requests)
game_state = {
    'finger_count': 0,
    'extended_fingers': [],
    'palm_facing': False,
    'frame_data': None,
    'frame_timestamp': 0,
    'last_frame_time': 0
}

# Video capture
cap = None
lock = threading.Lock()
FPS_TARGET = 15  # Target 15 FPS for smoother performance
process_thread = None
thread_alive = False
thread_errors = []

# Helper function to calculate distance
def distance(p1, p2):
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2 + (p1.z - p2.z)**2)

# Helper function for vector
def vec(a, b):
    return np.array([b.x - a.x, b.y - a.y, b.z - a.z], dtype=float)

def is_palm_facing_camera(hand_landmarks):
    """Estimate whether the palm is facing the camera."""
    lm = hand_landmarks.landmark
    wrist = lm[0]
    index_mcp = lm[5]
    pinky_mcp = lm[17]
    
    v1 = np.array([index_mcp.x - wrist.x, index_mcp.y - wrist.y, index_mcp.z - wrist.z])
    v2 = np.array([pinky_mcp.x - wrist.x, pinky_mcp.y - wrist.y, pinky_mcp.z - wrist.z])
    normal = np.cross(v1, v2)
    
    tips = [lm[4], lm[8], lm[12], lm[16], lm[20]]
    avg_tips_z = sum([t.z for t in tips]) / len(tips)
    
    palm_toward = (normal[2] < 0) or (avg_tips_z < wrist.z)
    return bool(palm_toward)

def count_extended_fingers(hand_landmarks):
    """Count extended fingers using angle-based detection."""
    lm = hand_landmarks.landmark
    
    extended = []
    
    # Finger indices: thumb, index, middle, ring, pinky
    finger_indices = {
        0: (1, 2, 3, 4),   # thumb: CMC, MCP, IP, TIP
        1: (5, 6, 8),      # index: MCP, PIP, TIP
        2: (9, 10, 12),    # middle
        3: (13, 14, 16),   # ring
        4: (17, 18, 20)    # pinky
    }
    
    COS_THRESHOLD = -0.5
    
    for f in range(5):
        if f == 0:
            # Thumb: use vectors tip->ip and ip->mcp
            tip = lm[4]
            ip = lm[3]
            mcp = lm[2]
            v1 = vec(ip, tip)
            v2 = vec(ip, mcp)
        else:
            mcp = lm[finger_indices[f][0]]
            pip = lm[finger_indices[f][1]]
            tip = lm[finger_indices[f][2]]
            v1 = vec(pip, tip)
            v2 = vec(pip, mcp)
        
        denom = (np.linalg.norm(v1) * np.linalg.norm(v2))
        cosang = 1.0
        if denom > 1e-6:
            cosang = np.dot(v1, v2) / denom
        
        if cosang < COS_THRESHOLD:
            extended.append(f)
    
    palm = is_palm_facing_camera(hand_landmarks)
    return len(extended), extended, palm

def init_camera():
    """Initialize camera capture."""
    global cap
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("ERROR: Cannot open camera")
            return False
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        cap.set(cv2.CAP_PROP_FPS, 30)
        print("Camera initialized successfully")
        return True
    except Exception as e:
        print(f"ERROR initializing camera: {e}")
        return False

def process_frame():
    """Process video frames continuously."""
    global cap, game_state, thread_alive, thread_errors
    
    frame_count = 0
    frame_skip = 0  # Skip frames for better performance
    thread_alive = True
    
    print("Frame processing thread started")
    
    while thread_alive:
        try:
            if cap is None:
                time.sleep(0.1)
                continue
            
            success, frame = cap.read()
            if not success:
                time.sleep(0.1)
                continue
            
            # Skip frames for performance
            frame_skip += 1
            if frame_skip % 2 == 0:
                continue
            
            try:
                frame = cv2.flip(frame, 1)
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            except Exception as e:
                print(f"ERROR: Frame conversion failed: {e}")
                thread_errors.append(str(e))
                time.sleep(0.05)
                continue
            
            # Process hand detection with timeout
            try:
                results = hands.process(rgb_frame)
            except Exception as e:
                print(f"ERROR in hand detection: {e}")
                thread_errors.append(f"Hand detection: {e}")
                time.sleep(0.05)
                continue
            
            total_fingers = 0
            all_extended = []
            palm_facing = False
            
            if results.multi_hand_landmarks:
                try:
                    for hand_landmarks in results.multi_hand_landmarks:
                        try:
                            count, extended, palm = count_extended_fingers(hand_landmarks)
                            total_fingers += count
                            all_extended.extend(extended)
                            palm_facing = palm
                            
                            # Draw hand skeleton
                            mp_drawing.draw_landmarks(
                                frame,
                                hand_landmarks,
                                mp_hands.HAND_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                                mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2)
                            )
                        except Exception as e:
                            print(f"ERROR processing individual hand: {e}")
                            thread_errors.append(f"Hand processing: {e}")
                            continue
                except Exception as e:
                    print(f"ERROR in hand landmarks loop: {e}")
                    thread_errors.append(f"Landmarks loop: {e}")
                    continue
            
            # Encode frame to base64 with quality reduction
            frame_data = None
            try:
                _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
                if buffer is not None:
                    frame_data = base64.b64encode(buffer).decode('utf-8')
            except Exception as e:
                print(f"ERROR encoding frame: {e}")
                thread_errors.append(f"Encoding: {e}")
                frame_data = None
            
            # Update game state (quick lock to prevent blocking)
            try:
                if lock.acquire(timeout=0.5):
                    try:
                        game_state['finger_count'] = total_fingers
                        game_state['extended_fingers'] = all_extended
                        game_state['palm_facing'] = palm_facing
                        game_state['frame_timestamp'] = time.time()
                        if frame_data:
                            game_state['frame_data'] = frame_data
                    finally:
                        lock.release()
                else:
                    print("WARNING: Could not acquire lock in time")
            except Exception as e:
                print(f"ERROR updating game state: {e}")
                thread_errors.append(f"Game state: {e}")
            
            frame_count += 1
            
            # Rate limiting
            try:
                time.sleep(1.0 / FPS_TARGET)
            except:
                pass
            
        except Exception as e:
            print(f"ERROR in main frame loop: {e}")
            print(traceback.format_exc())
            thread_errors.append(f"Main loop: {e}")
            time.sleep(0.1)
    
    print("Frame processing thread stopped")
    thread_alive = False

# Start background thread for frame processing
def start_processing():
    global process_thread
    if not init_camera():
        print("ERROR: Failed to initialize camera")
        return False
    process_thread = threading.Thread(target=process_frame, daemon=True, name="FrameProcessor")
    process_thread.start()
    print("Frame processing thread started")
    return True
    thread.start()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/frame')
def get_frame():
    """Get current frame as base64 image."""
    try:
        with lock:
            if game_state['frame_data']:
                return jsonify({
                    'image': game_state['frame_data'],
                    'finger_count': game_state['finger_count'],
                    'extended_fingers': game_state['extended_fingers'],
                    'palm_facing': game_state['palm_facing'],
                    'timestamp': game_state['frame_timestamp']
                })
    except Exception as e:
        print(f"Error in get_frame: {e}")
    
    return jsonify({'error': 'No frame available'}), 503

@app.route('/api/status')
def get_status():
    """Get current game state."""
    with lock:
        return jsonify({
            'finger_count': game_state['finger_count'],
            'extended_fingers': game_state['extended_fingers'],
            'palm_facing': game_state['palm_facing']
        })

@app.route('/api/health')
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'camera': cap is not None and cap.isOpened(),
        'thread_alive': thread_alive,
        'frame_data_available': game_state['frame_data'] is not None,
        'recent_errors': thread_errors[-5:] if thread_errors else []
    })

@app.route('/favicon.ico')
def favicon():
    """Serve a simple favicon to prevent 404 errors."""
    # Minimal 1x1 transparent PNG
    png_data = base64.b64decode(
        'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=='
    )
    return send_file(BytesIO(png_data), mimetype='image/png')

if __name__ == '__main__':
    print("\n" + "="*60)
    print("Starting Finger Detection Backend...")
    print("="*60)
    print(f"Target FPS: {FPS_TARGET}")
    print(f"Max hands: 2")
    print(f"Detection confidence: 0.7")
    print("="*60 + "\n")
    
    if start_processing():
        try:
            print("Starting Flask server on http://0.0.0.0:5000")
            print("Open browser at: http://localhost:5000")
            print("Press Ctrl+C to stop\n")
            app.run(debug=False, host='0.0.0.0', port=5000, threaded=True, use_reloader=False)
        except KeyboardInterrupt:
            print("\n\nShutting down...")
            thread_alive = False
            if cap:
                cap.release()
            print("Cleanup complete")
        except Exception as e:
            print(f"ERROR: {e}")
            traceback.print_exc()
    else:
        print("ERROR: Could not start processing")
        sys.exit(1)
