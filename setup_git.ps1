#!/usr/bin/env powershell
# Git Setup Script for Finger Counter Game
# Run this AFTER installing Git from https://git-scm.com/download/win

Write-Host "🚀 Setting up Git repository..." -ForegroundColor Green

# Navigate to project
cd "d:\personal project\hand_count_fingers"
Write-Host "📁 In project directory" -ForegroundColor Green

# Configure Git (first time only)
Write-Host "⚙️  Configuring Git..." -ForegroundColor Yellow
git config --global user.name "Ananya"
git config --global user.email "your.email@gmail.com"

# Initialize repository
Write-Host "📦 Initializing repository..." -ForegroundColor Yellow
git init
Write-Host "✓ Repository initialized" -ForegroundColor Green

# Add all files
Write-Host "📝 Adding files..." -ForegroundColor Yellow
git add .
Write-Host "✓ Files added" -ForegroundColor Green

# Create initial commit
Write-Host "💾 Creating commit..." -ForegroundColor Yellow
git commit -m "Initial commit: Finger counter game with Flask backend"
Write-Host "✓ Commit created" -ForegroundColor Green

# Rename to main branch
Write-Host "🔀 Setting up main branch..." -ForegroundColor Yellow
git branch -M main
Write-Host "✓ Main branch ready" -ForegroundColor Green

# Add remote
Write-Host "🌐 Adding GitHub remote..." -ForegroundColor Yellow
git remote add origin https://github.com/Ananyachy2001/finger-counter-game.git
Write-Host "✓ Remote added" -ForegroundColor Green

# Push to GitHub
Write-Host "📤 Pushing to GitHub..." -ForegroundColor Yellow
git push -u origin main
Write-Host "✓ Pushed successfully!" -ForegroundColor Green

Write-Host "`n✅ Done! Check your repository at:" -ForegroundColor Green
Write-Host "   https://github.com/Ananyachy2001/finger-counter-game" -ForegroundColor Cyan
