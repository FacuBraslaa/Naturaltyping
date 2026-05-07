import time
import random
import argparse
import sys
from pynput.keyboard import Controller, Key
from google_drive_integration import GoogleDocsTyper

# A simplified representation of the QWERTY keyboard for hand assignment
QWERTY_LAYOUT = {
    'left_hand': "qwertyasdfghzxcvbn ",
    'right_hand': "uiopjklm,./;'[]",
    'home_row_left': "asdf",
    'home_row_right': "jkl;"
}

# Adjacency map for more realistic typos (simplified)
ADJACENCY_MAP = {
    'q': 'wa', 'w': 'qeas', 'e': 'wrdf', 'r': 'etfg', 't': 'rygh', 'y': 'tuhj', 'u': 'yijk', 'i': 'uolk', 'o': 'ipkl', 'p': 'ol',
    'a': 'qwsz', 's': 'awedxz', 'd': 'serfcx', 'f': 'drtgvc', 'g': 'ftyhbv', 'h': 'gyujnb', 'j': 'huikmn', 'k': 'jiolm', 'l': 'kop',
    'z': 'asx', 'x': 'zsdc', 'c': 'xdfv', 'v': 'cfgb', 'b': 'vghn', 'n': 'bhjm', 'm': 'njk'
}

class NaturalTyper:
    def __init__(self, speed=0.15, error_rate=0.03):
        self.avg_typing_speed = speed
        self.error_prob = error_rate
        self.keyboard = Controller()
        self.last_hand = None

    def get_hand(self, char):
        """Determines which hand a character is typically typed with."""
        char_lower = char.lower()
        if char_lower in QWERTY_LAYOUT['left_hand']:
            return 'left'
        elif char_lower in QWERTY_LAYOUT['right_hand']:
            return 'right'
        return None

    def get_typo_char(self, char):
        """Returns a likely typo character based on keyboard adjacency."""
        char_lower = char.lower()
        if char_lower in ADJACENCY_MAP:
            return random.choice(ADJACENCY_MAP[char_lower])
        # Fallback to random char if not in map or uppercase/symbol
        return random.choice('qwertyuiopasdfghjklzxcvbnm')

    def type_text(self, text):
        """
        Mimics a slower, less efficient human typist on a QWERTY keyboard.
        """
        print(f"Typing starting in 5 seconds... Switch to your target application.")
        time.sleep(5)
        
        for char in text:
            # Determine current and previous character hands
            current_hand = self.get_hand(char)

            # Adjust delay based on typing dynamics
            typing_delay = random.uniform(self.avg_typing_speed * 0.8, self.avg_typing_speed * 1.5)

            # Longer pause for same-hand transitions, especially on the same row
            if self.last_hand and self.last_hand == current_hand:
                typing_delay += random.uniform(0.05, 0.15)
            # Faster for alternating hands
            elif self.last_hand and self.last_hand != current_hand:
                typing_delay = random.uniform(self.avg_typing_speed * 0.4, self.avg_typing_speed * 0.9)

            # Add a longer "thinking" pause after spaces or punctuation
            if char in ['.', '!', '?', ','] or (char == ' ' and random.random() < 0.25):
                typing_delay += random.uniform(0.5, 1.5)

            # Simulate a typo and correction
            if random.random() < self.error_prob:
                typo_char = self.get_typo_char(char)
                self.keyboard.type(typo_char)
                time.sleep(random.uniform(0.1, 0.3))
                self.keyboard.tap(Key.backspace)
                typing_delay += random.uniform(0.2, 0.5)  # A short delay for correction

            # Wait and then type the character
            time.sleep(typing_delay)

            if char == ' ':
                self.keyboard.tap(Key.space)
            else:
                self.keyboard.type(char)

            self.last_hand = current_hand
        
        print("\nTyping complete.")


class GoogleNaturalTyper:
    def __init__(self, speed=0.15, error_rate=0.03, credentials_path="credentials.json", user_email=None):
        """Initialize Google Docs natural typer."""
        self.avg_typing_speed = speed
        self.error_prob = error_rate
        self.last_hand = None
        self.docs_typer = GoogleDocsTyper(credentials_path, user_email=user_email)
    
    def get_hand(self, char):
        """Determines which hand a character is typically typed with."""
        char_lower = char.lower()
        if char_lower in QWERTY_LAYOUT['left_hand']:
            return 'left'
        elif char_lower in QWERTY_LAYOUT['right_hand']:
            return 'right'
        return None

    def get_typo_char(self, char):
        """Returns a likely typo character based on keyboard adjacency."""
        char_lower = char.lower()
        if char_lower in ADJACENCY_MAP:
            return random.choice(ADJACENCY_MAP[char_lower])
        return random.choice('qwertyuiopasdfghjklzxcvbnm')

    def type_to_google_doc(self, document_id, text, insert_index=1):
        """
        Write text to a Google Doc with human-like timing.
        
        Args:
            document_id: Google Doc ID
            text: Text to write
            insert_index: Position to insert at (default: 1 = start)
        """
        print(f"Starting to type in Google Doc...")
        
        for idx, char in enumerate(text):
            current_hand = self.get_hand(char)

            # Calculate typing delay
            typing_delay = random.uniform(self.avg_typing_speed * 0.8, self.avg_typing_speed * 1.5)

            if self.last_hand and self.last_hand == current_hand:
                typing_delay += random.uniform(0.05, 0.15)
            elif self.last_hand and self.last_hand != current_hand:
                typing_delay = random.uniform(self.avg_typing_speed * 0.4, self.avg_typing_speed * 0.9)

            if char in ['.', '!', '?', ','] or (char == ' ' and random.random() < 0.25):
                typing_delay += random.uniform(0.5, 1.5)

            # Simulate typo with correction
            if random.random() < self.error_prob:
                typo_char = self.get_typo_char(char)
                self.docs_typer.insert_text(document_id, typo_char, index=insert_index)
                time.sleep(random.uniform(0.1, 0.3))
                # Delete the typo
                self.docs_typer.delete_text(document_id, insert_index - 1, insert_index)
                typing_delay += random.uniform(0.2, 0.5)

            # Wait and insert character
            time.sleep(typing_delay)
            self.docs_typer.insert_text(document_id, char, index=insert_index)
            insert_index += 1  # Update insert position
            
            self.last_hand = current_hand
            print(f"Progress: {idx + 1}/{len(text)}", end='\r')
        
        print("\n✓ Typing complete in Google Doc!")

def main():
    parser = argparse.ArgumentParser(description="Natural Typing Simulator")
    parser.add_argument("--file", help="Path to a text file to type")
    parser.add_argument("--text", help="Text string to type")
    parser.add_argument("--speed", type=float, default=0.15, help="Average typing speed in seconds (default: 0.15)")
    parser.add_argument("--error-rate", type=float, default=0.03, help="Probability of making a typo (default: 0.03)")
    parser.add_argument("--drive", action="store_true", help="Type into Google Docs instead of keyboard")
    parser.add_argument("--doc-name", help="Name of Google Doc to create or use (with --drive)")
    parser.add_argument("--doc-id", help="ID of existing Google Doc (with --drive)")
    parser.add_argument("--credentials", default="credentials.json", help="Path to Google OAuth2 credentials (default: credentials.json)")
    parser.add_argument("--user", help="Gmail address for multi-user support (optional). Creates separate token per user.")
    parser.add_argument("--list-users", action="store_true", help="List all available Gmail accounts with tokens")
    parser.add_argument("--section", help="Section/heading name to write in (searches for this text in the document)")
    parser.add_argument("--list-sections", help="List all sections in a document (requires --doc-id or --doc-name)")
    
    args = parser.parse_args()
    
    # List available users
    if args.list_users:
        tokens = GoogleDocsTyper.list_available_tokens()
        if tokens:
            print("Available Gmail accounts:")
            for token in tokens:
                if token == 'token.pickle':
                    print("  - Default user (no email specified)")
                else:
                    email = token.replace('token_', '').replace('.pickle', '').replace('_at_', '@').replace('_', '.')
                    print(f"  - {email}")
        else:
            print("No tokens found. Authenticate with --drive first.")
        return
    
    # List sections in a document
    if args.list_sections:
        if not args.doc_id and not args.list_sections:
            print("Error: Specify --doc-id or use with --doc-name")
            sys.exit(1)
        
        google_docs = GoogleDocsTyper(credentials_path=args.credentials, user_email=args.user)
        
        doc_id = args.doc_id
        if not doc_id and args.list_sections != True:
            doc_id = google_docs.get_document_id(args.list_sections)
        
        if doc_id:
            sections = google_docs.list_sections(doc_id)
            if sections:
                print(f"Sections found in document:")
                for i, section in enumerate(sections, 1):
                    print(f"  {i}. {section}")
            else:
                print("No sections found in document.")
        else:
            print(f"Document not found.")
        return

    if not args.file and not args.text:
        # Default behavior if no arguments provided (backward compatibility or demo)
        text_to_type = """Una estrategia  clave es usar la palabra primero para la "escucha" antes que para la "denuncia". Para que haya reconciliación, la palabra debe usarse para validar el dolor de la víctima; que la víctima pueda hablar y ser escuchada. Recién después, la palabra puede usarse para proponer justicia y un futuro juntos, como hace Mijá, que primero denuncia la corrupción pero luego ofrece una visión de paz  para todos."""
        print("No input provided. Using default demo text.")
    elif args.file:
        try:
            with open(args.file, 'r') as f:
                text_to_type = f.read()
        except FileNotFoundError:
            print(f"Error: File '{args.file}' not found.")
            sys.exit(1)
    else:
        text_to_type = args.text

    # Google Drive mode
    if args.drive:
        google_typer = GoogleNaturalTyper(speed=args.speed, error_rate=args.error_rate, credentials_path=args.credentials, user_email=args.user)
        
        # Get or create document
        doc_id = None
        if args.doc_id:
            doc_id = args.doc_id
        elif args.doc_name:
            # Try to find existing doc
            doc_id = google_typer.docs_typer.get_document_id(args.doc_name)
            if not doc_id:
                print(f"Creating new Google Doc: '{args.doc_name}'...")
                doc_id = google_typer.docs_typer.create_document(args.doc_name)
        else:
            print("Error: Specify --doc-name or --doc-id with --drive")
            sys.exit(1)
        
        if not doc_id:
            print("Error: Could not create or find document.")
            sys.exit(1)
        
        if args.user:
            print(f"Using Gmail: {args.user}")
        print(f"Document ID: {doc_id}")
        
        # Handle section-based writing
        insert_index = 1
        if args.section:
            print(f"Searching for section: '{args.section}'...")
            found_index = google_typer.docs_typer.find_section_index(doc_id, args.section)
            if found_index:
                insert_index = found_index
                print(f"Found section. Writing after it...")
            else:
                print(f"Warning: Section '{args.section}' not found. Writing at the beginning.")
        
        google_typer.type_to_google_doc(doc_id, text_to_type, insert_index=insert_index)
    else:
        # Local keyboard mode (original functionality)
        typer = NaturalTyper(speed=args.speed, error_rate=args.error_rate)
        typer.type_text(text_to_type)

if __name__ == '__main__':
    main()