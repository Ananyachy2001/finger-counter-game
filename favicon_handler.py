import base64
from flask import send_from_directory

# Add this to serve a simple favicon to avoid 404 errors
@app.route('/favicon.ico')
def favicon():
    """Serve a simple favicon to prevent 404 errors."""
    # Create a minimal 1x1 transparent PNG
    png_data = base64.b64decode(
        'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=='
    )
    return png_data, 200, {'Content-Type': 'image/png'}
