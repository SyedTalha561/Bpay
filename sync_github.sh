#!/usr/bin/env bash
# BPAY Automated GitHub Sync Runner
# Ensures all project code is always organized, staged, committed, and pushed to SyedTalha561/Bpay

set -e

REPO_NAME="Bpay"
GITHUB_USER="SyedTalha561"
REMOTE_URL="git@github.com:${GITHUB_USER}/${REPO_NAME}.git"

echo "=========================================================="
echo "  ⚡ Syncing ${REPO_NAME} to GitHub (${GITHUB_USER}/${REPO_NAME})"
echo "=========================================================="

# Ensure remote is correct
git remote set-url origin "$REMOTE_URL" 2>/dev/null || git remote add origin "$REMOTE_URL"

# Check if there are changes
if [[ -n $(git status --porcelain) ]]; then
  echo "Found updated files. Staging and committing..."
  git add .
  COMMIT_MSG="chore(sync): automated sync of latest ${REPO_NAME} code ($(date '+%Y-%m-%d %H:%M:%S'))"
  git commit -m "$COMMIT_MSG"
else
  echo "Working tree is clean. Ready to push latest commits."
fi

# Push to GitHub
echo "Pushing to GitHub..."
git push -u origin main

echo "=========================================================="
echo "  ✓ Successfully synced ${REPO_NAME} to GitHub!"
echo "  👉 Repository: https://github.com/${GITHUB_USER}/${REPO_NAME}"
echo "=========================================================="
