#!/bin/bash

# Naturaltyping Installer for macOS

echo "Starting Naturaltyping installation..."

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3 and try again."
    exit 1
fi

echo "Python 3 found."

# Create virtual environment
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
else
    echo "Virtual environment already exists."
fi

# Activate virtual environment and install dependencies
echo "Installing dependencies..."
source .venv/bin/activate
pip install --upgrade pip
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "Error: requirements.txt not found!"
    exit 1
fi

# Create run wrapper
echo "Creating run wrapper script..."
cat << 'EOF' > run_naturaltyping.sh
#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/.venv/bin/activate"
python "$SCRIPT_DIR/main.py" "$@"
EOF

chmod +x run_naturaltyping.sh

echo ""
echo "Installation complete!"
echo "You can now run the tool using: ./run_naturaltyping.sh"
echo ""
echo "For keyboard typing:"
echo "  ./run_naturaltyping.sh --text 'Hello World'"
echo ""
echo "For Google Drive typing (requires setup):"
echo "  1. Follow instructions in GOOGLE_DRIVE_SETUP.md"
echo "  2. Then run: ./run_naturaltyping.sh --drive --doc-name 'Test' --text 'Hello'"
echo ""
echo "Note: You may need to grant Accessibility permissions to your terminal."

