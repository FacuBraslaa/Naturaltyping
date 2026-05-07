# Google Drive Integration Setup Guide

## Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click on "Select a Project" and create a new project
3. Name it "Naturaltyping" (or your preferred name)

## Step 2: Enable Required APIs

1. In the Cloud Console, go to "APIs & Services" > "Library"
2. Search for and enable:
   - **Google Docs API**
   - **Google Drive API**

## Step 3: Create OAuth 2.0 Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click the blue "+ CREATE CREDENTIALS" button at the top
3. Select "OAuth 2.0 Client ID"
4. You'll see a dialog saying "To create an OAuth client ID, you must first set up your OAuth consent screen"
   - Click "CONFIGURE CONSENT SCREEN"
   - Choose "External" as the User Type
   - Fill in the app name (e.g., "Naturaltyping")
   - Add your email address
   - Click "Save and Continue"
   - You can skip optional scopes, just click "Save and Continue"
   - Review and click "Back to Dashboard"

5. Click "+ CREATE CREDENTIALS" again
6. Select "OAuth 2.0 Client ID"
7. Choose "Desktop application" from the dropdown
8. Give it a name (e.g., "Naturaltyping Desktop")
9. Click "CREATE"

### Download the File

10. A modal will appear showing your credentials
11. Click the **"DOWNLOAD"** button (usually on the right side)
    - This downloads a JSON file (name may be like `client_secret_XXXXXX.json`)

12. **Move and rename** the downloaded file:
    ```bash
    # Navigate to your project folder
    cd ~/Documents/GitHub/Naturaltyping
    
    # Move the file and rename it
    mv ~/Downloads/client_secret_*.json ./credentials.json
    ```

13. Verify the file is in place:
    ```bash
    ls -la credentials.json
    # Should show: credentials.json
    ```

## Step 4: First-Time Authentication

Run any command with `--drive` flag for the first time:

```bash
./run_naturaltyping.sh --drive --doc-name "Test Document" --text "Hello World"
```

This will:
- Open a browser to authenticate with your Google account
- Save a `token.pickle` file for future use
- Create/use the specified Google Doc

## Usage Examples

### Create and type in a new Google Doc

```bash
./run_naturaltyping.sh --drive --doc-name "My Document" --text "Your text here"
```

### Type into an existing Google Doc (using ID)

```bash
./run_naturaltyping.sh --drive --doc-id "DOCUMENT_ID_HERE" --text "More text"
```

### Type from a file into Google Drive

```bash
./run_naturaltyping.sh --drive --doc-name "Document from File" --file my_file.txt
```

### Adjust typing speed and error rate

```bash
./run_naturaltyping.sh --drive --doc-name "Fast Typing" --text "Text" --speed 0.05 --error-rate 0.01
```

### Write to a specific section in the document

If your document has multiple sections/headings, you can write to a specific one:

```bash
# List all sections in the document first
./run_naturaltyping.sh --drive --doc-id "DOCUMENT_ID" --list-sections

# Write in a specific section
./run_naturaltyping.sh --drive --doc-id "DOCUMENT_ID" --text "Your text" --section "Section 2"
```

**How it works:**
- The tool searches for the section name/heading in the document
- Starts writing after that heading
- Without `--section`, writes at the beginning

## Getting Your Document ID

After creating a document, the ID will be printed. Or you can:

1. Open the Google Doc in your browser
2. Copy from the URL: `https://docs.google.com/document/d/{ID_HERE}/edit`

## Troubleshooting

### "credentials.json not found"
Make sure you've created and downloaded the OAuth2 credentials file from Google Cloud Console.

### "Authentication failed"
Delete `token.pickle` and run again. You'll need to re-authenticate.

### Permission denied errors
Ensure your Google Cloud project has the Docs and Drive APIs enabled.

## Multi-User Support

You can use Naturaltyping with multiple Gmail accounts on the same machine.

### How it works:
- Each Gmail account gets its own token file: `token_email_at_gmail_com.pickle`
- Use the `--user` parameter to specify which Gmail account to use

### Examples:

**First user (creates token automatically):**
```bash
./run_naturaltyping.sh --drive --doc-name "Doc1" --text "Hello" --user "person1@gmail.com"
```

**Second user (different token):**
```bash
./run_naturaltyping.sh --drive --doc-name "Doc2" --text "Hello" --user "person2@gmail.com"
```

**List all authenticated accounts:**
```bash
./run_naturaltyping.sh --list-users
```

Output example:
```
Available Gmail accounts:
  - person1@gmail.com
  - person2@gmail.com
  - Default user (no email specified)
```

### Notes:
- Each user needs to authenticate once (browser will open)
- Each user gets a separate token file for security
- Without `--user`, it uses the default token
- All users share the same `credentials.json`

## Security Notes

- **Never share `credentials.json`** with others
- **Keep `token.pickle` private** - it contains your authentication token
- Add both files to `.gitignore` if using version control
