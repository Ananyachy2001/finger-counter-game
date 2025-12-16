# 🔧 Deployment Troubleshooting Guide

Your code is now on GitHub! Let's fix the deployment issue. Answer these questions to diagnose:

---

## ❓ QUESTION 1: Which platform are you trying?

- [ ] **Railway.app** → Go to Section A
- [ ] **Netlify** → Go to Section B
- [ ] **Render** → Go to Section C
- [ ] **Heroku** → Go to Section D
- [ ] Don't know yet → Start with Railway (easiest!)

---

## 🚂 SECTION A: Railway Deployment Issues

### Issue A1: "Build Failed" Error

**Most Common Cause**: MediaPipe installation timeout

**Fix**:
1. Edit `requirements.txt`:
```
Flask==2.3.3
Flask-CORS==4.0.0
opencv-python-headless==4.8.1.78
mediapipe==0.8.11
numpy==1.24.3
Werkzeug==2.3.7
gunicorn==21.2.0
```

**Key change**: Use `opencv-python-headless` (not regular opencv-python)

2. Commit and push:
```powershell
$git = "C:\Program Files\Git\bin\git.exe"
& $git add requirements.txt
& $git commit -m "Use headless OpenCV for cloud"
& $git push origin main
```

3. In Railway dashboard:
   - Click your project
   - Click **Redeploy** button
   - Wait 3-5 minutes

### Issue A2: "App Crashes" After Deploy

**Cause**: Missing Python Procfile or wrong start command

**Fix**: Create `Procfile` in root directory:
```
web: gunicorn app:app
```

Push:
```powershell
& $git add Procfile
& $git commit -m "Add Procfile for Railway"
& $git push origin main
```

Redeploy on Railway.

### Issue A3: "Port Already in Use" Error

**Cause**: Your app is trying to run on port 5000 but Railway uses dynamic ports

**Fix**: Edit `app.py` - Find this line (~340):
```python
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
```

**Change to**:
```python
import os
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
```

Push and redeploy.

### Issue A4: "Cannot Find requirements.txt"

**Cause**: File is in wrong location or misspelled

**Fix**: Check file exists:
```powershell
Test-Path "d:\personal project\hand_count_fingers\requirements.txt"
```

Should return `True`. If False, create it.

### Issue A5: "500 Internal Server Error"

**Cause**: Backend error (usually camera or MediaPipe issue)

**Fix**: 
1. Go to Railway dashboard
2. Click your project
3. Click **Logs** tab
4. Look for red error messages
5. Copy the error message
6. See "How to Read Error Messages" section below

---

## 🎨 SECTION B: Netlify Deployment Issues

### Issue B1: "Build Failed"

**Most Common Cause**: Wrong build command

**Fix**: Go to Netlify dashboard:
1. Click your site
2. Click **Site settings**
3. Click **Build & deploy**
4. Click **Edit settings**
5. Find "Build command"
6. Change to: `echo "Frontend ready"`
7. Find "Publish directory"
8. Change to: `dist`
9. Save
10. Click **Trigger deploy** button
11. Wait 2 minutes

### Issue B2: "Blank Page" When Opened

**Cause**: Frontend can't connect to backend

**Fix**:
1. Open your Netlify URL
2. Press F12 (open Developer Console)
3. Look for red error messages
4. Common error: "Cannot GET /api/health"
5. **Solution**: Your backend URL is wrong

**Update backend URL**:
1. Edit `templates/index.html`
2. Find line ~447:
```javascript
function getApiUrl() {
    const localhost = 'http://localhost:5000/api';
    const production = 'https://your-railway-url/api';
    ...
}
```
3. Replace `your-railway-url` with your actual Railway URL
4. Don't include `/api` at the end
5. Should look like: `https://finger-counter-backend-prod-xxxx.up.railway.app`

Example:
```javascript
const production = 'https://finger-counter-backend-prod-abc123.up.railway.app/api';
```

6. Save file
7. Commit and push:
```powershell
& $git add templates/index.html
& $git commit -m "Update backend URL"
& $git push origin main
```
8. Netlify auto-deploys (wait 1-2 min)

### Issue B3: "Cannot Find dist/ Folder"

**Cause**: dist folder not in repository

**Fix**: Create it:
```powershell
mkdir "d:\personal project\hand_count_fingers\dist" -Force
cp "d:\personal project\hand_count_fingers\templates\index.html" "d:\personal project\hand_count_fingers\dist\index.html"
```

Then push:
```powershell
& $git add dist/
& $git commit -m "Add dist folder for Netlify"
& $git push origin main
```

Trigger redeploy on Netlify.

### Issue B4: "Video Shows But No Detection"

**Cause**: Backend is down or API is failing

**Fix**:
1. Check your Railway backend is running
   - Go to Railway dashboard
   - Check for green "Running" status
2. If not running: Click **Redeploy**
3. Wait 30 seconds
4. Refresh Netlify page

---

## ⚙️ SECTION C: Render Deployment Issues

### Issue C1: "Pre-receive Hook Declined"

**Cause**: `.venv` folder in git (like we had before!)

**Fix**: 
1. Remove .venv from git:
```powershell
$git = "C:\Program Files\Git\bin\git.exe"
& $git rm -r --cached .venv
& $git commit -m "Remove .venv from tracking"
& $git push origin main
```

2. Make sure `.gitignore` has:
```
.venv/
__pycache__/
*.pyc
```

3. Deploy again on Render

### Issue C2: "Build Fails - Cannot Install MediaPipe"

**Fix**: Edit `requirements.txt`:
```
opencv-python-headless==4.8.1.78
```

### Issue C3: "Spins Down After 15 Minutes"

**This is normal for free tier!** First request takes 30-60 seconds.

**If you want instant response**: Upgrade to paid ($7/month) or use Railway instead.

---

## 🟣 SECTION D: Heroku Deployment Issues

### Issue D1: "Build Pack Detection Failed"

**Fix**: Make sure you have:
- ✅ `requirements.txt` in root
- ✅ `Procfile` in root
- ✅ `.gitignore` has `.venv`

### Issue D2: "Application Error" Page

**Cause**: App crashed on startup

**Fix**:
1. Check Heroku logs:
```powershell
# If you have Heroku CLI installed:
heroku logs --tail
```

2. If MediaPipe fails, use headless OpenCV:
```
opencv-python-headless==4.8.1.78
```

---

## 🔍 How to Read Error Messages

### Common Error: "ModuleNotFoundError: No module named 'mediapipe'"

**Means**: requirements.txt wasn't installed

**Fix**:
1. Check `requirements.txt` exists in root (not in subfolder)
2. Redeploy
3. If still fails, use headless version

### Common Error: "Port 5000 is already in use"

**Means**: App can't start on that port

**Fix**: Use environment port (see Section A, Issue A3)

### Common Error: "Cannot find module 'cv2'"

**Means**: OpenCV didn't install properly

**Fix**: 
```
pip install opencv-python-headless
```

Update requirements.txt and push.

---

## 📋 Quick Diagnostic Checklist

Before debugging, verify:

- [ ] Code is pushed to GitHub?
  ```powershell
  & $git log --oneline -3
  ```
  Should show your recent commits

- [ ] requirements.txt exists?
  ```powershell
  Test-Path "d:\personal project\hand_count_fingers\requirements.txt"
  ```
  Should return True

- [ ] app.py is in root?
  ```powershell
  Test-Path "d:\personal project\hand_count_fingers\app.py"
  ```
  Should return True

- [ ] templates/index.html exists?
  ```powershell
  Test-Path "d:\personal project\hand_count_fingers\templates\index.html"
  ```
  Should return True

- [ ] dist/index.html exists?
  ```powershell
  Test-Path "d:\personal project\hand_count_fingers\dist\index.html"
  ```
  Should return True

---

## 🚀 Step-by-Step: Fix and Redeploy

### For Railway:

```powershell
# 1. Fix requirements.txt
# Edit file, change opencv-python to opencv-python-headless

# 2. Commit
$git = "C:\Program Files\Git\bin\git.exe"
& $git add requirements.txt
& $git commit -m "Fix: use headless OpenCV"
& $git push origin main

# 3. Redeploy on Railway dashboard
# Click project → Click Redeploy → Wait 3-5 minutes
```

### For Netlify:

```powershell
# 1. Update backend URL
# Edit templates/index.html line ~447

# 2. Copy to dist
cp templates/index.html dist/index.html

# 3. Commit
& $git add templates/index.html dist/index.html
& $git commit -m "Update backend URL"
& $git push origin main

# 4. Netlify auto-deploys (wait 1-2 min)
```

---

## 💬 Get Help

**Tell me**:
1. Which platform (Railway/Netlify/Render/Heroku)?
2. What error message do you see?
3. Where do you see it (dashboard? console? email)?
4. What's the exact text?

**Then I can help fix it specifically!**

---

## ✅ Signs of Success

### Backend Deployed ✅
- Dashboard shows "Running" or "Deployed"
- You have a URL like `https://xxx.up.railway.app`
- Testing URL returns:
```json
{"status": "healthy", ...}
```

### Frontend Deployed ✅
- Dashboard shows "Published" or "Deployed"
- You have a URL like `https://xxx.netlify.app`
- Opening URL shows game page (not blank)
- F12 console has no red errors

### Both Working Together ✅
- Video stream shows
- Hand detection works
- Game plays through 10 rounds
- Finger counting is accurate

---

**What specific error are you getting? Let me know and I'll fix it!** 🔧
