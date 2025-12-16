# Deploy to Netlify + Render Backend

Deploy your finger counting game with **Netlify** for the frontend and **Render** for the Python backend.

## Why This Architecture?

- **Netlify**: Fast, free static hosting for your HTML/CSS/JavaScript frontend
- **Render**: Free tier for Python Flask backend (auto-deploys from GitHub)
- **CORS Enabled**: Frontend and backend can communicate seamlessly

---

## Step 1: Prepare Your Git Repository

### 1.1 Initialize Git (if not already done)

```bash
cd d:\personal project\hand_count_fingers
git init
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

### 1.2 Create `.gitignore`

Your `.gitignore` should already exclude `.venv` and `__pycache__`. Verify it has:

```
.venv/
__pycache__/
*.pyc
.DS_Store
.env
node_modules/
```

### 1.3 Add All Files and Commit

```bash
git add .
git commit -m "Initial commit: finger counting game with Flask backend"
```

### 1.4 Push to GitHub

```bash
# Create a NEW repository on GitHub at https://github.com/new
# Then run:

git remote add origin https://github.com/YOUR_USERNAME/hand_count_fingers.git
git branch -M main
git push -u origin main
```

---

## Step 2: Deploy Backend to Render

### 2.1 Create Render Account

1. Go to https://render.com
2. Click **Sign up** (or sign in with GitHub)
3. Link your GitHub account

### 2.2 Create New Web Service

1. Click **New +** → **Web Service**
2. Select your `hand_count_fingers` repository
3. Fill in these settings:

| Setting | Value |
|---------|-------|
| **Name** | `finger-counter-backend` |
| **Environment** | `Python 3` |
| **Region** | Pick closest to you |
| **Branch** | `main` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app` |

### 2.3 Add Environment Variables

1. Scroll to **Environment**
2. Click **Add Environment Variable**
3. Add:
   - **Key**: `FLASK_ENV`
   - **Value**: `production`

### 2.4 Click Deploy

- Render will automatically deploy your backend
- You'll get a URL like: `https://finger-counter-backend.onrender.com`
- **Copy this URL** - you'll need it in the next step

---

## Step 3: Update Frontend for Backend URL

### 3.1 Edit `templates/index.html`

Find this line (around line 450):

```javascript
const API_URL = 'http://localhost:5000';
```

Replace with:

```javascript
const API_URL = 'https://finger-counter-backend.onrender.com';
```

(Replace with your actual Render URL)

### 3.2 Commit and Push

```bash
git add templates/index.html
git commit -m "Update backend URL for Render deployment"
git push origin main
```

---

## Step 4: Deploy Frontend to Netlify

### 4.1 Prepare Frontend Files

Create a `dist` folder with your frontend:

```bash
mkdir -p dist
cp templates/index.html dist/index.html
```

### 4.2 Create Netlify Configuration

Create `netlify.toml`:

```toml
[build]
  publish = "dist"
  command = "echo 'Frontend ready'"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

### 4.3 Create Netlify Account

1. Go to https://app.netlify.com
2. Click **Sign up** (use GitHub for easy linking)
3. Authorize Netlify to access your GitHub repositories

### 4.4 Deploy from GitHub

1. Click **Add new site** → **Import an existing project**
2. Choose **GitHub**
3. Select your `hand_count_fingers` repository
4. Fill in settings:

| Setting | Value |
|---------|-------|
| **Branch to deploy** | `main` |
| **Build command** | `echo 'Frontend ready'` |
| **Publish directory** | `dist` |

5. Click **Deploy site**

Your site will be live at a URL like: `https://hand-count-fingers.netlify.app`

---

## Step 5: Enable CORS on Backend

Your Flask backend needs to allow requests from Netlify. Your `app.py` already has this:

```python
from flask_cors import CORS
CORS(app)
```

✅ Already configured! No changes needed.

---

## Step 6: Test Everything

1. Open your Netlify URL: `https://hand-count-fingers.netlify.app`
2. Allow camera access
3. Show your fingers and play the game
4. Verify the video streams and detection works

---

## Troubleshooting

### Issue: "Cannot connect to backend"

**Solution**: 
- Check your Render backend URL in `templates/index.html`
- Make sure you used the full HTTPS URL
- Give Render 2-3 minutes to deploy

### Issue: "CORS error"

**Solution**:
- Verify `CORS(app)` is in your `app.py`
- Restart your Render service by clicking **Manual Deploy**

### Issue: Video shows but no detection

**Solution**:
- Check Render logs: go to your service → **Logs**
- Check browser console (F12 → Console tab)
- Ensure your camera permissions are granted

### Issue: Blank video feed

**Solution**:
- Your Render free tier may have gone to sleep
- Click **Manual Deploy** on Render to wake it up
- Wait 30-60 seconds for it to start

---

## Important Notes

### Free Tier Limitations

- **Render**: Free tier spins down after 15 minutes of inactivity
  - First request will take 30-60 seconds to start
  - **Solution**: Upgrade to paid tier for $7/month for continuous uptime

- **Netlify**: No limitations on hosting
  - Automatically deploys when you push to GitHub
  - Very fast CDN delivery

### Camera Access

- Netlify and Render must use **HTTPS** (they do by default)
- Browser will ask for camera permission - grant it
- Works on mobile browsers too! (most of them)

### Performance Tips

1. Use a strong internet connection
2. Good lighting for better hand detection
3. Keep your hands in frame
4. 15 FPS streaming is optimized for low bandwidth

---

## Update Your Game (After Deployment)

### To update the frontend:

```bash
# Edit templates/index.html
# Then:
cp templates/index.html dist/index.html
git add dist/index.html templates/index.html
git commit -m "Update game UI"
git push origin main
# Netlify auto-deploys! ✅
```

### To update the backend:

```bash
# Edit app.py
# Then:
git add app.py
git commit -m "Improve finger detection"
git push origin main
# Render auto-deploys! ✅
```

---

## Advanced: Use Custom Domain

### On Netlify:

1. Go to your site settings → **Domain management**
2. Click **Add custom domain**
3. Enter your domain (e.g., `fingergame.com`)
4. Follow the DNS setup instructions

### On Render:

1. Go to your backend service → **Settings**
2. Scroll to **Custom Domain**
3. Add your API domain (e.g., `api.fingergame.com`)

---

## Quick Reference

| Component | Platform | Free | URL |
|-----------|----------|------|-----|
| Frontend (HTML/JS) | Netlify | ✅ | https://hand-count-fingers.netlify.app |
| Backend (Python/Flask) | Render | ✅* | https://finger-counter-backend.onrender.com |
| Repository | GitHub | ✅ | https://github.com/YOUR_USERNAME/hand_count_fingers |

*Render free tier: Spins down after 15 min. Upgrade to $7/month for always-on.

---

## Support

- **Netlify Docs**: https://docs.netlify.com
- **Render Docs**: https://render.com/docs
- **GitHub Help**: https://docs.github.com

Happy deploying! 🚀
