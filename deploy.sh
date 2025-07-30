#!/bin/bash
# Deploy script to update GitHub Pages

echo "Deploying to GitHub Pages..."

# Save current branch
CURRENT_BRANCH=$(git branch --show-current)

# Ensure we're on main and have latest changes
git checkout main
git pull origin main

# Switch to gh-pages
git checkout gh-pages

# Copy the latest game file
cp fighter_enhanced.html index.html

# Commit and push if there are changes
if git diff --quiet; then
    echo "No changes to deploy"
else
    git add index.html
    git commit -m "Update game from main branch"
    git push origin gh-pages
    echo "Deployed successfully!"
fi

# Switch back to original branch
git checkout $CURRENT_BRANCH

echo "Done! Changes will be live at https://frankywashere.github.io/elonfighter/ in a few minutes"