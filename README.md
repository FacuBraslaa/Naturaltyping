# Naturaltyping

Naturaltyping is a Python tool that simulates human typing behavior. It mimics the natural pauses, speed variations, and occasional typos (with corrections) that occur when a person types on a QWERTY keyboard.

## Features

- **Realistic Typing Simulation**: Variable typing speed and delays based on hand transitions and key adjacency.
- **Typo Simulation**: Occasional typos based on QWERTY keyboard layout, with automatic backspace correction.
- **CLI Support**: Run from the command line with custom text, files, speed, and error rates.
- **Hand Detection**: Logic to determine which hand types which character to adjust timing.
- **Google Drive Integration**: Type directly into Google Docs with human-like timing and typos.

## Installation

### macOS

We provide an automated installer script for macOS.

1.  Open your terminal.
2.  Navigate to the project directory.
3.  Run the installer:
    ```bash
    ./install_mac.sh
    ```

This script will:
- Check for Python 3.
- Create a virtual environment (`.venv`).
- Install necessary dependencies.
- Create a `run_naturaltyping.sh` wrapper for easy execution.

## Usage

After installation, you can use the `run_naturaltyping.sh` script to run the tool.

### Basic Usage

To type a specific string:

```bash
./run_naturaltyping.sh --text "Hello, this is a test."
```

To type the contents of a file:

```bash
./run_naturaltyping.sh --file my_document.txt
```

### Advanced Options

- `--speed`: Set the average typing speed in seconds (default: 0.15). Lower is faster.
- `--error-rate`: Set the probability of making a typo (default: 0.03).

**Example:**

```bash
./run_naturaltyping.sh --text "Fast typer!" --speed 0.05 --error-rate 0.01
```

### Manual Usage (without wrapper)

If you prefer to run it manually with Python:

1.  Activate the virtual environment:
    ```bash
    source .venv/bin/activate
    ```
2.  Run the script:
    ```bash
    python main.py --text "Your text here"
    ```

## Google Drive Integration

Type directly into Google Docs with human-like timing!

### Quick Start

1. **Setup Google Cloud credentials** (one-time setup):
   - Run: `bash setup_google_credentials.sh` (helper script)
   - Or follow [GOOGLE_DRIVE_SETUP.md](GOOGLE_DRIVE_SETUP.md) for detailed instructions

2. **Create and type into a new Google Doc**:
   ```bash
   ./run_naturaltyping.sh --drive --doc-name "My Document" --text "Your text here"
   ```

3. **Type into an existing Google Doc**:
   ```bash
   ./run_naturaltyping.sh --drive --doc-id "DOCUMENT_ID" --text "More text"
   ```

### Google Drive Examples

Type from a file:
```bash
./run_naturaltyping.sh --drive --doc-name "Document from File" --file input.txt
```

Adjust speed and typo rate:
```bash
./run_naturaltyping.sh --drive --doc-name "Slow Typing" --text "Text" --speed 0.2 --error-rate 0.05
```

**Multi-user support** (use different Gmail accounts):
```bash
# User 1
./run_naturaltyping.sh --drive --doc-name "Test" --text "Hola" --user "user1@gmail.com"

# User 2 (will create separate token)
./run_naturaltyping.sh --drive --doc-name "Test" --text "Hola" --user "user2@gmail.com"
```

**Write to specific sections** (useful for documents with multiple sections/tabs):
```bash
# List all sections in document
./run_naturaltyping.sh --drive --doc-id "DOCUMENT_ID" --list-sections

# Write to specific section
./run_naturaltyping.sh --drive --doc-id "DOCUMENT_ID" --text "Text" --section "Section Name"
```

List all authenticated Gmail accounts:
```bash
./run_naturaltyping.sh --list-users
```

For more details, see [GOOGLE_DRIVE_SETUP.md](GOOGLE_DRIVE_SETUP.md)

## Note

This tool uses `pynput` to control the keyboard. On macOS, you may need to grant "Accessibility" permissions to your terminal application (e.g., Terminal, iTerm2) in **System Preferences > Security & Privacy > Privacy > Accessibility**.
