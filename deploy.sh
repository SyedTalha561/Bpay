#!/usr/bin/env bash
# BPAY Global Launch & Local Runner Script

set -e

echo "=========================================================="
echo "  ⚡ BPAY Sovereign Benefactor Platform"
echo "  Direct Expense Clearance & Philanthropic Fintech"
echo "=========================================================="

PORT=8080

case "$1" in
  start|run|local)
    echo "Starting BPAY server on http://localhost:$PORT ..."
    python3 server.py
    ;;
  git)
    echo "Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial launch of BPAY platform"
    echo "Git initialized and initial commit created!"
    echo "To push to your GitHub: git remote add origin <your-repo-url> && git push -u origin main"
    ;;
  *)
    echo "Available commands:"
    echo "  ./deploy.sh start  -> Run local server on http://localhost:8080"
    echo "  ./deploy.sh git    -> Initialize git repository for GitHub / Vercel"
    echo ""
    echo "Running local server by default..."
    python3 server.py
    ;;
esac
