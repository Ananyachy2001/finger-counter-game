#!/usr/bin/env python
"""
Prepare for Netlify + Render deployment
Copies frontend files to dist folder for Netlify
"""

import os
import shutil
from pathlib import Path

def setup_deployment():
    """Prepare deployment files"""
    
    project_root = Path(__file__).parent
    dist_dir = project_root / 'dist'
    templates_dir = project_root / 'templates'
    
    # Create dist directory if it doesn't exist
    dist_dir.mkdir(exist_ok=True)
    print(f"✓ Created {dist_dir}")
    
    # Copy HTML files
    for html_file in templates_dir.glob('*.html'):
        shutil.copy2(html_file, dist_dir / html_file.name)
        print(f"✓ Copied {html_file.name}")
    
    # Create _redirects file for Netlify routing
    redirects_file = dist_dir / '_redirects'
    redirects_file.write_text('/*  /index.html  200\n')
    print(f"✓ Created _redirects file for SPA routing")
    
    # Create a simple README for the dist folder
    readme = dist_dir / 'README.md'
    readme.write_text('''# Frontend Distribution

This folder contains files deployed to Netlify.

## To Deploy:
1. Push changes to GitHub
2. Netlify automatically deploys from this folder

## Updating:
- Edit files in `templates/` folder
- Copy updated files here
- Commit and push to GitHub
''')
    print(f"✓ Created dist/README.md")
    
    print("\n✅ Deployment setup complete!")
    print("\nNext steps:")
    print("1. Commit changes: git add . && git commit -m 'Prepare for Netlify deployment'")
    print("2. Push to GitHub: git push origin main")
    print("3. Connect GitHub to Netlify: https://app.netlify.com")
    print("4. Select this repository and deploy!")

if __name__ == '__main__':
    setup_deployment()
