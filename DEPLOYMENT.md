# Finger Counter Game - Python Flask + Web Version

A full-stack finger counting game with:
- **Backend**: Python Flask with MediaPipe for accurate hand detection
- **Frontend**: Interactive web UI with real-time video feed
- **Deployment**: Ready for Heroku, Railway, or any Python hosting

## Features

✅ Accurate Python-based finger detection (MediaPipe)  
✅ Real-time hand skeleton visualization  
✅ Palm orientation detection (front/back)  
✅ Per-finger state display  
✅ 10-round scoring game  
✅ Web-based (works on any browser)  
✅ Mobile-responsive design  

## Project Structure

```
hand_count_fingers/
├── app.py                  # Flask backend with hand detection
├── requirements.txt        # Python dependencies
├── Procfile               # Heroku deployment config
├── templates/
│   └── index.html         # Web frontend (game UI)
└── README.md              # This file
```

## Local Setup & Testing

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Locally

```bash
python app.py
```

The server will start at `http://localhost:5000`

### 3. Open in Browser

Navigate to `http://localhost:5000` and start playing!

## How It Works

1. **Flask Backend** (`app.py`):
   - Captures video from your camera
   - Processes frames with MediaPipe Hands
   - Runs accurate finger counting algorithm (angle-based detection)
   - Detects palm orientation
   - Streams frames and detection data to frontend via `/api/frame`

2. **Web Frontend** (`templates/index.html`):
   - Displays live video feed from backend
   - Shows target number and current finger count
   - Displays per-finger states
   - Manages game logic and scoring
   - Provides real-time feedback

## Deploy to Heroku

### Option 1: Using Heroku CLI

```bash
# Install Heroku CLI
# (https://devcenter.heroku.com/articles/heroku-cli)

# Login to Heroku
heroku login

# Create a new Heroku app
heroku create your-app-name

# Add buildpack for Python
heroku buildpacks:add heroku/python

# Deploy
git push heroku main

# View logs
heroku logs --tail
```

### Option 2: Using GitHub (Automatic Deployment)

1. Push code to GitHub:
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/finger-counter-game.git
git push -u origin main
```

2. Connect to Heroku:
   - Go to [dashboard.heroku.com](https://dashboard.heroku.com)
   - Create new app → Connect to GitHub
   - Select your repository
   - Enable automatic deployments

## Deploy to Railway.app

Railway is easier than Heroku (no credit card required for free tier):

1. **Connect GitHub**:
   - Go to [railway.app](https://railway.app)
   - Click "New Project" → "Deploy from GitHub"
   - Authorize GitHub and select your repo

2. **Railway Auto-Detects**:
   - It automatically detects `Procfile` and `requirements.txt`
   - Sets up Python environment
   - Deploys automatically

3. **Done!** Your app is live

## Deploy to Render.com

1. Go to [render.com](https://render.com)
2. Create new "Web Service"
3. Connect GitHub repository
4. Build command: `pip install -r requirements.txt`
5. Start command: `gunicorn app:app`
6. Click Deploy

## Important Notes ⚠️

### Camera Access on Deployed Servers
- **Local**: Works perfectly (camera attached to your PC)
- **Deployed Server (Heroku/Railway)**: Won't work (server has no camera)

**Solution**: You need a **hybrid approach**:
1. Use **browser-based hand detection** for web (TensorFlow.js)
2. Use **server for complex logic** (optional)

### For Production with Web Cameras

Use the **HTML5 version** instead (`index.html` from pure JS):

```bash
# This version runs hand detection IN the browser
# Copy the standalone index.html to a hosting service:
# - Netlify (drag & drop)
# - GitHub Pages
# - Vercel
# - Any static host
```

### If You NEED Backend Processing

The current Flask app is useful if you want to:
- Process frames on a server with GPU
- Store results in a database
- Run complex ML models
- But **still won't work for camera on remote server**

## Configuration

### Adjust Detection Sensitivity

In `app.py`, line ~70:

```python
COS_THRESHOLD = -0.5  # Lower = stricter (fewer false positives)
                      # Higher = looser (more detections)
```

### Change Game Settings

In `templates/index.html`, around line 340:

```javascript
maxRounds: 10,  // Number of rounds
```

## Troubleshooting

**Backend not connecting?**
- Make sure `app.py` is running
- Check that port 5000 is not blocked
- Look for error messages in terminal

**Fingers not detected?**
- Ensure good lighting
- Keep entire hand visible
- Try different hand positions
- Check console for errors (F12)

**Deployed app shows "Cannot connect"?**
- The server probably can't access a camera (it's on a remote server)
- Use the TensorFlow.js version instead for web deployment

## Best Practices

1. **For Local/Personal Use**: Use this Flask version (most accurate)
2. **For Web Deployment**: Use TensorFlow.js version (browser-based)
3. **For Production**: Consider GPU acceleration on a powerful server

## Performance

- **Local**: 30+ FPS on modern PC
- **Server**: Depends on CPU/GPU available
- **Web (TF.js)**: 20-30 FPS on modern devices

## Future Improvements

- [ ] Add gesture recognition (thumbs up, peace sign, etc.)
- [ ] Multiplayer mode
- [ ] Difficulty levels (1-10 fingers)
- [ ] Sound effects
- [ ] Leaderboard (with database)
- [ ] Save game progress
- [ ] Custom hand models

## License

Free to use and modify for educational purposes.

---

**Happy gaming! 🎮🖐️**
