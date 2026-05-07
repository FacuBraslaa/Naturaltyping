#!/usr/bin/env python3
"""
Example usage of Naturaltyping with Google Drive integration.

This script demonstrates different ways to use the natural typing functionality
with Google Docs.
"""

from main import GoogleNaturalTyper, NaturalTyper

def example_local_typing():
    """Example: Type locally on keyboard"""
    print("=" * 50)
    print("Example 1: Local Keyboard Typing")
    print("=" * 50)
    
    typer = NaturalTyper(speed=0.1, error_rate=0.02)
    text = "This is a test of local keyboard typing!"
    
    print(f"Text to type: {text}")
    print("Starting in 5 seconds...")
    # typer.type_text(text)  # Uncomment to run


def example_google_drive_new_doc():
    """Example: Create new Google Doc and type into it"""
    print("\n" + "=" * 50)
    print("Example 2: Create New Google Doc")
    print("=" * 50)
    
    google_typer = GoogleNaturalTyper(speed=0.2, error_rate=0.03)
    
    # Create new document
    doc_id = google_typer.docs_typer.create_document("Naturaltyping Test Document")
    print(f"Created document with ID: {doc_id}")
    
    # Type into the document
    text = "Hello! This is being typed with natural human-like timing in Google Docs."
    print(f"Text to type: {text}")
    # google_typer.type_to_google_doc(doc_id, text)  # Uncomment to run


def example_google_drive_existing_doc():
    """Example: Type into existing Google Doc"""
    print("\n" + "=" * 50)
    print("Example 3: Type into Existing Google Doc")
    print("=" * 50)
    
    google_typer = GoogleNaturalTyper(speed=0.15, error_rate=0.02)
    
    # Use an existing document ID
    doc_id = "YOUR_DOCUMENT_ID_HERE"  # Replace with actual ID
    text = "Adding more content to an existing document..."
    
    print(f"Document ID: {doc_id}")
    print(f"Text to type: {text}")
    # google_typer.type_to_google_doc(doc_id, text)  # Uncomment to run


def example_google_drive_find_doc():
    """Example: Find document by name and type into it"""
    print("\n" + "=" * 50)
    print("Example 4: Find Document by Name")
    print("=" * 50)
    
    google_typer = GoogleNaturalTyper(speed=0.15, error_rate=0.03)
    
    # Find document by name
    doc_name = "My Test Document"
    doc_id = google_typer.docs_typer.get_document_id(doc_name)
    
    if doc_id:
        print(f"Found document '{doc_name}' with ID: {doc_id}")
        text = "Typing into a found document!"
        # google_typer.type_to_google_doc(doc_id, text)  # Uncomment to run
    else:
        print(f"Document '{doc_name}' not found.")


def example_custom_speed():
    """Example: Custom typing speeds for different scenarios"""
    print("\n" + "=" * 50)
    print("Example 5: Custom Typing Speeds")
    print("=" * 50)
    
    scenarios = [
        ("Very Fast", 0.05, 0.01),
        ("Normal", 0.15, 0.03),
        ("Slow", 0.25, 0.05),
        ("Very Slow", 0.4, 0.08),
    ]
    
    for name, speed, error_rate in scenarios:
        print(f"\n{name}: speed={speed}s, error_rate={error_rate}")
        typer = GoogleNaturalTyper(speed=speed, error_rate=error_rate)


if __name__ == "__main__":
    print("\nNaturaltyping - Google Drive Integration Examples")
    print("=" * 50)
    
    example_local_typing()
    example_google_drive_new_doc()
    example_google_drive_existing_doc()
    example_google_drive_find_doc()
    example_custom_speed()
    
    print("\n" + "=" * 50)
    print("Examples ready to use!")
    print("Uncomment the lines marked with '# Uncomment to run' to execute them.")
    print("=" * 50)
