# Finger Counter Game - Web Version

A fun, interactive game for kids to learn numbers by showing fingers to the camera. Built with TensorFlow.js for hand detection.

## Features

✅ Real-time hand detection using TensorFlow.js  
✅ Detects palm orientation (front/back)  
✅ Shows individual finger states  
✅ 10-round scoring game  
✅ Responsive design (mobile-friendly)  
✅ Instant feedback with animations  

## Local Testing

Simply open `index.html` in your browser. The game will request camera access.

```bash
# Option 1: Open directly
open index.html

# Option 2: Use a local server (recommended for better performance)
python -m http.server 8000
# Then visit: http://localhost:8000
```

## Deploy to Netlify

### Option 1: Drag & Drop (Easiest)

1. Go to [netlify.com](https://netlify.com)
2. Sign up for a free account
3. Drag and drop the `index.html` file onto the Netlify interface
4. Your game is now live!

### Option 2: GitHub Integration (Recommended)

1. **Create a GitHub repo**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/finger-counter-game.git
   git push -u origin main
   ```

2. **Connect to Netlify**
   - Go to [netlify.com](https://netlify.com)
   - Click "New site from Git"
   - Select GitHub and authorize
   - Choose your repository
   - Leave build settings empty (it's just static files)
   - Click "Deploy"

### Option 3: CLI Deployment

1. **Install Netlify CLI**
   ```bash
   npm install -g netlify-cli
   ```

2. **Deploy**
   ```bash
   netlify deploy --prod --dir=.
   ```

3. **Authentication**: Follow the prompts to log in to Netlify

## File Structure

```
hand_count_fingers/
├── index.html           # Main game (all-in-one file)
├── README.md            # This file
└── maze.py             # Original Python version (optional)
```

## How to Play

1. **Allow Camera Access**: Click "Start Game" and allow camera access
2. **Watch the Target**: The target number appears in the top-left
3. **Show Fingers**: Extend the correct number of fingers to your camera
4. **See Feedback**: 
   - Fingers are shown in green (extended) or gray (closed)
   - Palm orientation is detected (front/back)
   - Instruction text guides you
5. **Complete 10 Rounds**: Try to match as many numbers correctly as possible
6. **View Score**: See your final accuracy at the end

## Technical Details

**Hand Detection**: Uses TensorFlow.js MediaPipe Hands model
- Detects hand keypoints in real-time
- 21 keypoints per hand tracked
- Palm orientation detection using hand geometry

**Browser Compatibility**:
- Chrome/Edge: ✅ Full support
- Firefox: ✅ Full support
- Safari: ✅ Requires iOS 14.5+
- Mobile: ✅ Responsive design works on tablets

**Performance**:
- Smooth 30+ FPS detection on modern devices
- Lightweight (~5MB initial load)
- Runs entirely in the browser (no server required)

## Customization

### Change Number of Rounds
Edit line in JavaScript section:
```javascript
maxRounds: 10,  // Change this value
```

### Adjust Difficulty
Modify finger detection sensitivity (line ~280):
```javascript
if (tipPos.y < pipPos.y - 20) {  // Decrease value for easier detection
```

### Change Colors
Edit CSS gradient sections:
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

## Troubleshooting

**Camera not working?**
- Check browser permissions (Settings > Privacy > Camera)
- Try a different browser
- Ensure good lighting
- Move your hand closer to the camera

**Hand not detected?**
- Ensure your entire hand is visible
- Try a different lighting angle
- Move background away (plain wall is ideal)

**Slow performance?**
- Close other browser tabs
- Lower video quality in browser settings
- Try on a device with better hardware

## Future Enhancements

- Sound effects (beeps, celebrations)
- Hand gesture recognition (thumbs up, etc.)
- Multiplayer mode
- Different difficulty levels
- Gesture-based menus

## License

Free to use and modify for educational purposes.

## Support

For issues or feedback, please create an issue in the repository or contact the developer.

---

**Happy learning! 🎮🖐️**
