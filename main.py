import customtkinter as ctk
from gui_components import CodeSummarizerApp
import nltk
from language_patterns import get_supported_languages

def main():
    # Download NLTK resources
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('wordnet', quiet=True)

    # Set up the main window
    ctk.set_appearance_mode("system")  # Modes: system (default), light, dark
    ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

    # Create and run the application
    root = ctk.CTk()
    root.title("Multi-Language Code Summarizer")
    
    # Set initial and minimum window size
    root.geometry("800x600")
    root.minsize(600, 500)  # Minimum width and height
    
    app = CodeSummarizerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
