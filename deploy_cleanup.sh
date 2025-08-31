#!/bin/bash

echo
echo "========================================"
echo " JAI GURU DEV AI - Railway Deployment"
echo "========================================"
echo

echo "🧹 Cleaning up development artifacts..."

# Remove cleanup folder (development artifacts)
if [ -d "cleanup" ]; then
    echo "Removing cleanup folder..."
    rm -rf cleanup
    echo "✅ Removed cleanup folder"
else
    echo "✅ Cleanup folder already removed"
fi

echo
echo "🐍 Removing Python cache files..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true
find . -name "*.pyo" -delete 2>/dev/null || true
echo "✅ Python cache files cleaned"

echo
echo "🗑️ Removing temporary files..."
find . -name "*.tmp" -delete 2>/dev/null || true
find . -name "*.log" -delete 2>/dev/null || true
find . -name "*~" -delete 2>/dev/null || true
find . -name "*.bak" -delete 2>/dev/null || true
echo "✅ Temporary files cleaned"

echo
echo "========================================"
echo "✅ CLEANUP COMPLETED SUCCESSFULLY!"
echo "========================================"
echo
echo "Your JAI GURU DEV AI Chatbot is now ready for Railway deployment!"
echo
echo "Next steps:"
echo "1. git add ."
echo "2. git commit -m 'Prepare for Railway deployment'"
echo "3. git push origin main"
echo "4. Deploy to Railway using RAILWAY_DEPLOYMENT_GUIDE.md"
echo
echo "🚂 Happy deploying! 🙏"