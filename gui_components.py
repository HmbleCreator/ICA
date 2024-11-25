import customtkinter as ctk
from tkinter import messagebox, filedialog
import re
import os
import sys
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from language_patterns import get_supported_languages, get_language_patterns

class CodeSummarizerApp(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        
        # Configure the grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=3)  # Code input area
        self.grid_rowconfigure(6, weight=2)  # Summary area
        
        # Pack the frame to fill the entire window
        self.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        self.title_label = ctk.CTkLabel(
            self, 
            text="Multi-Language Code Summarizer", 
            font=("Helvetica", 20, "bold")
        )
        self.title_label.grid(row=0, column=0, pady=(0, 20), sticky="ew")

        # Language and File Selection Frame
        self.top_frame = ctk.CTkFrame(self)
        self.top_frame.grid(row=1, column=0, pady=10, sticky="ew")
        self.top_frame.grid_columnconfigure(1, weight=1)

        # Language Selection
        self.language_label = ctk.CTkLabel(
            self.top_frame, 
            text="Language:", 
            font=("Helvetica", 14)
        )
        self.language_label.grid(row=0, column=0, padx=(0, 10), sticky="w")

        supported_languages = get_supported_languages()
        self.language_var = ctk.StringVar()
        self.language_combo = ctk.CTkComboBox(
            self.top_frame, 
            values=[lang.capitalize() for lang in supported_languages],
            variable=self.language_var,
            state="readonly",
            width=200
        )
        self.language_combo.set(supported_languages[0].capitalize())
        self.language_combo.grid(row=0, column=1, sticky="ew", padx=(0, 10))

        # File Selection Button
        self.file_button = ctk.CTkButton(
            self.top_frame, 
            text="Open File", 
            command=self.open_file,
            width=100
        )
        self.file_button.grid(row=0, column=2, sticky="e")

        # Code Input Section
        self.code_label = ctk.CTkLabel(
            self, 
            text="Code Input:", 
            font=("Helvetica", 14)
        )
        self.code_label.grid(row=2, column=0, pady=(10, 5), sticky="w")

        # Code Input Textbox with Scrollbar
        self.code_text = ctk.CTkTextbox(
            self, 
            corner_radius=10,
            font=("Consolas", 12),
            wrap="none"  # Disable word wrapping
        )
        self.code_text.grid(row=4, column=0, pady=10, sticky="nsew")

        # Buttons Frame
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.grid(row=5, column=0, pady=10, sticky="ew")
        self.button_frame.grid_columnconfigure((0,1), weight=1)

        # Summarize Button
        self.summarize_button = ctk.CTkButton(
            self.button_frame, 
            text="Generate Summary", 
            command=self.summarize,
            corner_radius=10,
            font=("Helvetica", 14, "bold")
        )
        self.summarize_button.grid(row=0, column=0, padx=10, sticky="ew")

        # Clear Button
        self.clear_button = ctk.CTkButton(
            self.button_frame, 
            text="Clear", 
            command=self.clear_input,
            corner_radius=10,
            fg_color="gray",
            hover_color="darkgray"
        )
        self.clear_button.grid(row=0, column=1, padx=10, sticky="ew")

        # Summary Section
        self.summary_label = ctk.CTkLabel(
            self, 
            text="Code Summary:", 
            font=("Helvetica", 14)
        )
        self.summary_label.grid(row=6, column=0, pady=(10, 5), sticky="w")

        # Summary Textbox
        self.summary_text = ctk.CTkTextbox(
            self, 
            corner_radius=10,
            state="disabled",
            font=("Helvetica", 12)
        )
        self.summary_text.grid(row=7, column=0, pady=10, sticky="nsew")

    def open_file(self):
        """Open and read a file"""
        try:
            # Open file dialog
            file_path = filedialog.askopenfilename(
                title="Select Code File",
                filetypes=[
                    ("Python Files", "*.py"),
                    ("JavaScript Files", "*.js"),
                    ("Java Files", "*.java"),
                    ("All Files", "*.*")
                ]
            )
            
            # If a file is selected
            if file_path:
                # Determine language from file extension
                file_extension = os.path.splitext(file_path)[1][1:].lower()
                language_map = {
                    'py': 'python',
                    'js': 'javascript',
                    'java': 'java'
                }
                language = language_map.get(file_extension, file_extension)
                
                # Read file contents
                with open(file_path, 'r') as file:
                    code_contents = file.read()
                
                # Clear existing content
                self.code_text.delete("1.0", "end")
                
                # Insert file contents
                self.code_text.insert("1.0", code_contents)
                
                # Set language in combo box
                if language.capitalize() in self.language_combo['values']:
                    self.language_combo.set(language.capitalize())
        except Exception as e:
            messagebox.showerror("File Open Error", str(e))

    def clear_input(self):
        """Clear code input and summary areas"""
        self.code_text.delete("1.0", "end")
        self.summary_text.configure(state="normal")
        self.summary_text.delete("1.0", "end")
        self.summary_text.configure(state="disabled")

    def summarize(self):
        """Generate and display code summary"""
        # Extract code and language
        code = self.code_text.get("1.0", "end-1c")
        language = self.language_var.get().lower()

        # Validate input
        if not code.strip():
            messagebox.showwarning("Warning", "Please enter some code to summarize.")
            return

        # Generate summary
        try:
            summary = self.extract_code_structure(code, language)
            
            # Update summary text
            self.summary_text.configure(state="normal")
            self.summary_text.delete("1.0", "end")
            self.summary_text.insert("end", summary)
            self.summary_text.configure(state="disabled")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def extract_code_structure(self, code, language):
        """Generate a comprehensive summary of the code."""
        patterns = get_language_patterns(language)
        if not patterns:
            return f"Unsupported language: {language}"

        # Clean comments first
        code_clean = re.sub(patterns['comment_multi'], '', code)
        code_clean = re.sub(patterns['comment_single'], '', code_clean)

        # Extract structure
        structure = {
            'classes': re.findall(patterns['class'], code_clean),
            'functions': self.extract_function_details(code, patterns),
            'imports': re.findall(patterns['import'], code_clean),
            'modules': patterns['module_used'],
            'module_purposes': patterns['module_purposes']
        }

        # Preprocess and extract key terms
        tokens = self.preprocess_code(code, language)
        key_terms = self.extract_key_terms(tokens)

        # Build summary
        summary = []
        
        # Basic description
        summary.append(f"This code is written in {language.capitalize()}.")
        
        # Classes
        if structure['classes']:
            main_class = structure['classes'][0]
            summary.append(f"It defines a main class '{main_class}' and {len(structure['classes'])-1} additional class(es).")
        
        # Functions
        if structure['functions']:
            summary.append("The code includes several key functions:")
            for func_name, args in structure['functions'].items():
                args_text = ", ".join(args) if args else "no arguments"
                summary.append(f"- '{func_name}' takes {len(args)} argument(s) ({args_text})")
        
        # Libraries and their purposes
        detected_modules = set(structure['modules']).intersection(
            module for imp in structure['imports'] 
            for module in structure['modules'] 
            if module.lower() in imp.lower()
        )
        
        for module in detected_modules:
            purpose = structure['module_purposes'].get(module)
            if purpose:
                summary.append(f"The '{module}' module is used to {purpose}.")
        
        # Key terms
        summary.append(f"Key concepts in the code include: {', '.join(key_terms)}.")

        return " ".join(summary)

    def extract_function_details(self, code, patterns):
        """Extract function names and their arguments."""
        functions = {}
        
        # Clean comments first
        code_clean = re.sub(patterns['comment_multi'], '', code)
        code_clean = re.sub(patterns['comment_single'], '', code_clean)
        
        # Find functions and their arguments
        func_matches = re.finditer(patterns['function'], code_clean)
        for match in func_matches:
            func_name = next(group for group in match.groups() if group is not None)
            # Find arguments for this function
            arg_match = re.search(patterns['arguments'], match.group())
            args = []
            if arg_match:
                args_str = arg_match.group(1)
                if args_str:
                    args = [arg.strip() for arg in args_str.split(',')]
            functions[func_name] = args
        
        return functions

    def preprocess_code(self, code, language):
        """Preprocess code for key terms extraction."""
        patterns = get_language_patterns(language)
        if not patterns:
            return []

        # Remove comments
        code = re.sub(patterns['comment_multi'], '', code)
        code = re.sub(patterns['comment_single'], '', code)
        
        # Split camelCase and snake_case
        code = re.sub(r'([a-z0-9])([A-Z])', r'\1 \2', code)
        code = code.replace('_', ' ')
        
        tokens = word_tokenize(code.lower())
        stop_words = set(stopwords.words('english'))
        tokens = [token for token in tokens if token.isalpha() and token not in stop_words]
        lemmatizer = WordNetLemmatizer()
        tokens = [lemmatizer.lemmatize(token) for token in tokens]
        return tokens

    def extract_key_terms(self, tokens, n=5):
        """Extract the most common terms from the code."""
        freq_dist = nltk.FreqDist(tokens)
        return [term for term, _ in freq_dist.most_common(n)]