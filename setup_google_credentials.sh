#!/bin/bash
# Helper script to set up Google Drive credentials

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "================================"
echo "Google Drive Setup Helper"
echo "================================"
echo ""

# Check if credentials already exist
if [ -f "$PROJECT_DIR/credentials.json" ]; then
    echo "✓ credentials.json already exists!"
    echo "  Location: $PROJECT_DIR/credentials.json"
    echo ""
    exit 0
fi

echo "📝 Steps to get your credentials:"
echo ""
echo "1. Go to: https://console.cloud.google.com/"
echo "2. Create a new project or select existing one"
echo "3. Enable APIs: Google Docs API + Google Drive API"
echo "4. Go to 'APIs & Services' > 'Credentials'"
echo "5. Click '+ CREATE CREDENTIALS'"
echo "6. Select 'OAuth 2.0 Client ID'"
echo "7. If asked, configure OAuth Consent Screen first:"
echo "   - Choose 'External'"
echo "   - Fill app name"
echo "   - Add your email"
echo "   - Save & Continue"
echo "8. Then create 'Desktop application' credentials"
echo "9. Click 'DOWNLOAD' in the popup"
echo ""
echo "================================"
echo ""

# Look for downloaded credentials file
DOWNLOADS_DIR="$HOME/Downloads"
FOUND_FILE=""

if ls "$DOWNLOADS_DIR"/client_secret_*.json 1> /dev/null 2>&1; then
    FOUND_FILE=$(ls -t "$DOWNLOADS_DIR"/client_secret_*.json | head -n1)
    echo "✓ Found credentials file in Downloads:"
    echo "  $FOUND_FILE"
    echo ""
    
    read -p "Do you want to use this file? (y/n) " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cp "$FOUND_FILE" "$PROJECT_DIR/credentials.json"
        echo ""
        echo "✓ Successfully copied to: $PROJECT_DIR/credentials.json"
        echo ""
        echo "You're ready to use Google Drive!"
        echo ""
        echo "Try running:"
        echo "  ./run_naturaltyping.sh --drive --doc-name 'Test' --text 'Hello'"
        exit 0
    fi
fi

echo "Manual Setup:"
echo "1. Download the credentials.json from Google Cloud Console"
echo "2. Save it to: $PROJECT_DIR/credentials.json"
echo ""
echo "Or copy with:"
echo "  cp ~/Downloads/client_secret_*.json $PROJECT_DIR/credentials.json"
echo ""
