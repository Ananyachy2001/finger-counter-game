# Git Installation & Push Guide

## ⚠️ Problem
You got: `error: src refspec main does not match any`

This means **Git is not installed** on your system.

---

## ✅ Solution: Install Git on Windows

### Method 1: Download Installer (Recommended)
1. Go to https://git-scm.com/download/win
2. Click **64-bit Git for Windows Setup**
3. Run the installer
4. Click **Next** through all screens (defaults are fine)
5. Restart PowerShell after installation

### Method 2: Using Chocolatey (if you have it)
```powershell
choco install git
```

### Method 3: Using Windows Package Manager
```powershell
winget install Git.Git
```

---

## After Installing Git

### 1. Configure Git (First Time Only)
```powershell
git config --global user.name "Your Name"
git config --global user.email "your.email@gmail.com"
```

### 2. Navigate to Your Project
```powershell
cd "d:\personal project\hand_count_fingers"
```

### 3. Initialize Git Repository
```powershell
git init
git add .
git commit -m "Initial commit: Finger counter game"
```

### 4. Add Remote and Push
```powershell
git remote add origin https://github.com/Ananyachy2001/finger-counter-game.git
git branch -M main
git push -u origin main
```

---

## If You Already Have a Git Repository

Check your current branch:
```powershell
git branch
```

If it shows nothing or shows a different branch name:
```powershell
# Switch or create main branch
git branch -M main

# Then push
git push -u origin main
```

---

## Complete Step-by-Step for Your Project

After installing Git, run these commands in PowerShell:

```powershell
# 1. Go to your project
cd "d:\personal project\hand_count_fingers"

# 2. Configure Git (first time only)
git config --global user.name "Ananya"
git config --global user.email "your.email@gmail.com"

# 3. Initialize or reset repository
git init

# 4. Add all files
git add .

# 5. Create initial commit
git commit -m "Initial commit: Finger counter game with Flask backend"

# 6. Rename branch to main (if needed)
git branch -M main

# 7. Add your GitHub repository
git remote add origin https://github.com/Ananyachy2001/finger-counter-game.git

# 8. Push to GitHub
git push -u origin main
```

---

## Verify Installation Worked

After these steps, go to:
https://github.com/Ananyachy2001/finger-counter-game

You should see all your files uploaded! ✅

---

## Still Having Issues?

### Issue: "fatal: not a git repository"
**Solution**: Make sure you're in the right folder
```powershell
cd "d:\personal project\hand_count_fingers"
git init
git add .
git commit -m "Initial commit"
```

### Issue: "Permission denied" or "Authentication failed"
**Solution**: Use personal access token instead of password
1. Go to https://github.com/settings/tokens
2. Click "Generate new token"
3. Give it "repo" and "workflow" permissions
4. Use this token as your password

### Issue: ".venv folder is too large"
**Solution**: Make sure `.gitignore` excludes it
```
.venv/
__pycache__/
*.pyc
```

Your `.gitignore` already has this, so it should be fine.

---

## Next: Netlify Deployment

Once your code is on GitHub, you can:
1. Go to https://app.netlify.com
2. Click "Import from GitHub"
3. Select your `finger-counter-game` repository
4. Deploy! 🚀

---

**Still stuck?** Run this to verify your setup:
```powershell
git --version
git config --global user.name
git config --global user.email
```

This will show if Git is installed and configured correctly.
