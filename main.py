import time
import random
import argparse
import sys
from pynput.keyboard import Controller, Key

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

def main():
    parser = argparse.ArgumentParser(description="Natural Typing Simulator")
    parser.add_argument("--file", help="Path to a text file to type")
    parser.add_argument("--text", help="Text string to type")
    parser.add_argument("--speed", type=float, default=0.15, help="Average typing speed in seconds (default: 0.15)")
    parser.add_argument("--error-rate", type=float, default=0.03, help="Probability of making a typo (default: 0.03)")
    
    args = parser.parse_args()

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

    typer = NaturalTyper(speed=args.speed, error_rate=args.error_rate)
    typer.type_text(text_to_type)

if __name__ == '__main__':
    main()