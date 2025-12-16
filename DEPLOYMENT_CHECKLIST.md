# 🚀 Finger Counter Game - Deployment Checklist

## Pre-Deployment ✅

### Local Setup
- [ ] App runs perfectly locally at `http://localhost:5000`
- [ ] Video frames stream continuously
- [ ] Finger detection works accurately
- [ ] Game completes all 10 rounds without crashing

### Code Quality
- [ ] No console errors (F12 → Console)
- [ ] All imports/dependencies are in `requirements.txt`
- [ ] `.gitignore` excludes `.venv/`, `__pycache__/`, etc.
- [ ] `app.py` has `CORS(app)` enabled

### Files Prepared
- [ ] `dist/index.html` is updated and ready
- [ ] `dist/_redirects` file exists
- [ ] `netlify.toml` is configured
- [ ] `requirements.txt` has all dependencies

---

## GitHub Setup 🔗

### Step 1: Create GitHub Repository
```bash
cd "d:\personal project\hand_count_fingers"
git init
git add .
git commit -m "Initial commit: Finger counter game"
```

### Step 2: Push to GitHub
```bash
# Create new repo at https://github.com/new
# Name it: hand_count_fingers

git remote add origin https://github.com/YOUR_USERNAME/hand_count_fingers.git
git branch -M main
git push -u origin main
```

### Checklist
- [ ] Repository created on GitHub
- [ ] Code pushed to GitHub
- [ ] Branch is named `main`
- [ ] `.gitignore` is working (no `.venv/` folder in repo)

---

## Backend Deployment (Render) 🐍

### Step 1: Create Render Account
- Go to https://render.com
- Sign up with GitHub

### Step 2: Create Web Service
- Click **New +** → **Web Service**
- Select your GitHub repository
- Settings:
  - **Name**: `finger-counter-backend`
  - **Environment**: `Python 3`
  - **Branch**: `main`
  - **Build Command**: `pip install -r requirements.txt`
  - **Start Command**: `gunicorn app:app`

### Step 3: Deploy
- Click **Deploy**
- Wait 2-3 minutes for deployment
- You'll get a URL like: `https://finger-counter-backend.onrender.com`

### Checklist
- [ ] Render account created
- [ ] Repository connected
- [ ] Service deployed successfully
- [ ] **Copy Backend URL**: `_____________________________`

---

## Frontend Deployment (Netlify) 🎨

### Step 1: Update Backend URL
1. Open `templates/index.html`
2. Find line ~447: `return 'https://finger-counter-backend.onrender.com/api';`
3. Replace with your actual Render URL
4. Copy to `dist/index.html`
5. Commit and push

```bash
git add templates/index.html dist/index.html
git commit -m "Update backend URL for Netlify"
git push origin main
```

### Step 2: Create Netlify Account
- Go to https://app.netlify.com
- Click **Sign up** (use GitHub for easier linking)

### Step 3: Deploy from GitHub
- Click **Add new site** → **Import an existing project**
- Choose **GitHub**
- Select `hand_count_fingers` repository
- Deploy settings:
  - **Branch**: `main`
  - **Build command**: `echo 'Frontend ready'`
  - **Publish directory**: `dist`
- Click **Deploy site**

### Step 4: Wait for Deployment
- Netlify will show build logs
- Once successful, you'll get a URL like: `https://hand-count-fingers.netlify.app`

### Checklist
- [ ] Netlify account created and GitHub connected
- [ ] Repository deployed to Netlify
- [ ] Build completed successfully
- [ ] **Frontend URL**: `_____________________________`

---

## Testing 🧪

### Live Site Testing
1. Open your Netlify URL in browser
2. Grant camera permission
3. Test these:
   - [ ] Video feed appears
   - [ ] Hand detection works (show your hand)
   - [ ] Finger counting is accurate
   - [ ] Game logic works (completes rounds)
   - [ ] Scoring system works
   - [ ] Can play multiple games

### Troubleshooting Common Issues

**Issue**: "Cannot connect to backend"
- **Fix**: Check that your Render backend URL is correct in `templates/index.html`
- **Fix**: Make sure Render service is running (check Render dashboard)
- **Fix**: Give it 30 seconds on first request (free tier spins down)

**Issue**: "CORS Error in console"
- **Fix**: Verify `CORS(app)` is in your `app.py` (line ~14)
- **Fix**: Restart the Render service by clicking **Manual Deploy**

**Issue**: "Video shows but no detection"
- **Fix**: Check browser console (F12) for JavaScript errors
- **Fix**: Grant camera permissions when prompted
- **Fix**: Ensure good lighting for hand detection

**Issue**: "Blank video feed"
- **Fix**: Render free tier spins down - first request takes 30-60 seconds
- **Fix**: Click **Manual Deploy** on Render to wake it up
- **Fix**: Refresh page and wait 1-2 minutes

---

## Ongoing Maintenance 📝

### Update Frontend
1. Edit `templates/index.html`
2. Copy to `dist/index.html`
3. Commit and push to GitHub
4. Netlify auto-deploys! ✅

```bash
cp templates/index.html dist/index.html
git add templates/index.html dist/index.html
git commit -m "Update game UI"
git push origin main
```

### Update Backend
1. Edit `app.py`
2. Commit and push to GitHub
3. Render auto-deploys! ✅

```bash
git add app.py
git commit -m "Improve detection algorithm"
git push origin main
```

### Monitor Live App
- **Frontend**: https://app.netlify.com (click your site to see deployments)
- **Backend**: https://dashboard.render.com (click your service to see logs)

---

## Upgrade for Production 💰

### Netlify
- Free tier: Perfect for the game, no upgrades needed
- Paid tier: $20+/month (not needed unless scaling)

### Render
- Free tier: Service sleeps after 15 minutes of inactivity
  - **Drawback**: First request takes 30-60 seconds to start
  - **Great for**: Testing, low-traffic projects
  
- Paid tier: $7/month for "Standard" (always on)
  - **Benefit**: No spin-down, instant responses
  - **Perfect for**: Smooth gameplay, production use

**Recommendation**: Start with free tier for testing, upgrade to Render paid ($7/mo) for always-on backend.

---

## Final Deployment Summary

| Component | Platform | Cost | URL |
|-----------|----------|------|-----|
| **Frontend** | Netlify | Free | `https://YOUR_SITE.netlify.app` |
| **Backend** | Render | Free* | `https://YOUR_BACKEND.onrender.com` |
| **Repository** | GitHub | Free | `https://github.com/YOUR_USERNAME/hand_count_fingers` |

*Free tier included, upgrade to $7/mo for always-on

---

## Quick Reference Commands

```bash
# Check status
git status

# Update and deploy frontend
cp templates/index.html dist/index.html
git add -A
git commit -m "Update frontend"
git push origin main

# View logs
# Frontend: https://app.netlify.com
# Backend: https://dashboard.render.com
```

---

## Need Help? 📞

- **Netlify Docs**: https://docs.netlify.com
- **Render Docs**: https://render.com/docs
- **GitHub Docs**: https://docs.github.com
- **Flask Docs**: https://flask.palletsprojects.com
- **MediaPipe Docs**: https://developers.google.com/mediapipe

---

**Status**: Ready for deployment! 🎉

Last updated: December 16, 2025
