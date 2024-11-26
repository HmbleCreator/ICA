# gui_components.py
import customtkinter as ctk
from tkinter import messagebox, filedialog
import re
import os
import ast
import nltk
from nltk.corpus import stopwords
from typing import Dict, Any
import language_patterns

class LanguageSummarizer:
    @staticmethod
    def get_language(code: str) -> str:
        """
        Infer the programming language based on code characteristics.
        
        Args:
            code (str): Source code to analyze
        
        Returns:
            str: Detected language (lowercase)
        """
        # Prioritized language detection checks
        language_checks = [
            ('python', r'def\s+\w+'),
            ('java', r'(public|private|protected)\s+class'),
            ('javascript', r'(function\s+\w+|const\s+\w+\s*=\s*\(.*\)\s*=>)'),
            ('cpp', r'#include\s*[<"]'),
            ('go', r'func\s+\w+\s*\('),
            ('php', r'\<\?php'),
            ('ruby', r'def\s+\w+')
        ]
        
        for lang, pattern in language_checks:
            if re.search(pattern, code, re.MULTILINE):
                return lang
        
        return 'python'  # Default to Python

    @staticmethod
    def summarize_code(code: str, language: str) -> str:
        """
        Generate a comprehensive summary of code for different languages.
        
        Args:
            code (str): Source code to analyze
            language (str): Programming language
        
        Returns:
            str: Detailed code summary
        """
        # Retrieve language-specific patterns
        lang_patterns = language_patterns.get_language_patterns(language)
        
        if not lang_patterns:
            return f"Summarization for {language} is not yet supported."
        
        # Extract key information based on language patterns
        summary_parts = []
        
        try:
            # Remove comments
            code_no_comments = re.sub(lang_patterns['comment_single'], '', code)
            code_no_comments = re.sub(lang_patterns.get('comment_multi', r''), '', code_no_comments, flags=re.DOTALL)
            
            # Find classes
            classes = re.findall(lang_patterns['class'], code_no_comments, re.MULTILINE)
            if classes:
                summary_parts.append(f"Defines {len(classes)} class(es): {', '.join(classes)}")
            
            # Find functions
            functions = re.findall(lang_patterns['function'], code_no_comments, re.MULTILINE)
            functions = [f for f in functions if f]  # Remove empty matches
            if functions:
                summary_parts.append(f"Contains {len(functions)} function(s): {', '.join(functions[:10])}")
                
                # Analyze function arguments if possible
                if 'arguments' in lang_patterns:
                    arg_matches = re.findall(lang_patterns['arguments'], code_no_comments, re.MULTILINE)
                    if arg_matches:
                        arg_details = [
                            f"{func}: {len(re.findall(r'\w+', args or ''))}"
                            for func, args in zip(functions[:10], arg_matches)
                        ]
                        summary_parts.append(f"Function arguments: {', '.join(arg_details)}")
            
            # Find imports/includes
            imports = re.findall(lang_patterns['import'], code, re.MULTILINE)
            if imports:
                unique_imports = list(set(imports))
                summary_parts.append(f"Imports {len(unique_imports)} module(s): {', '.join(unique_imports[:5])}")
            
            # Module purposes
            used_modules = [
                module for module in lang_patterns.get('module_used', []) 
                if any(module in str(imp) for imp in imports)
            ]
            if used_modules:
                module_desc = [
                    lang_patterns['module_purposes'].get(module, module) 
                    for module in used_modules
                ]
                summary_parts.append(f"Modules used for: {', '.join(module_desc)}")
            
            # Key terms extraction
            try:
                tokens = [
                    word for word in re.findall(r'\b\w+\b', code_no_comments.lower()) 
                    if word not in set(stopwords.words('english'))
                ]
                freq_dist = nltk.FreqDist(tokens)
                key_terms = [term for term, _ in freq_dist.most_common(5)]
                summary_parts.append(f"Key concepts: {', '.join(key_terms)}")
            except Exception:
                pass
            
            # Code complexity metrics
            lines = code.split('\n')
            summary_parts.append(f"Total lines of code: {len(lines)}")
            
        except Exception as e:
            summary_parts.append(f"Error during analysis: {str(e)}")
        
        return " ".join(summary_parts) if summary_parts else "Could not generate a comprehensive summary."

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

        # Get supported languages from language_patterns module
        supported_languages = [lang.capitalize() for lang in language_patterns.get_supported_languages()]
        supported_languages.insert(0, "Auto Detect")
        
        self.language_var = ctk.StringVar(value="Auto Detect")
        self.language_combo = ctk.CTkComboBox(
            self.top_frame, 
            values=supported_languages,
            variable=self.language_var,
            state="readonly",
            width=200
        )
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

        # Code Input Textbox
        self.code_text = ctk.CTkTextbox(
            self, 
            corner_radius=10,
            font=("Consolas", 12),
            wrap="none"
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
            file_path = filedialog.askopenfilename(
                title="Select Code File",
                filetypes=[
                    ("All Supported Files", "*.py *.java *.js *.cpp *.go *.php *.rb"),
                    ("Python Files", "*.py"),
                    ("Java Files", "*.java"),
                    ("JavaScript Files", "*.js"),
                    ("C++ Files", "*.cpp"),
                    ("Go Files", "*.go"),
                    ("PHP Files", "*.php"),
                    ("Ruby Files", "*.rb"),
                    ("All Files", "*.*")
                ]
            )
            
            if file_path:
                with open(file_path, 'r', encoding='utf-8') as file:
                    code_contents = file.read()
                
                self.code_text.delete("1.0", "end")
                self.code_text.insert("1.0", code_contents)
                
                # Auto-detect or set language based on file extension
                file_ext = os.path.splitext(file_path)[1].lower()
                ext_to_lang = {
                    '.py': 'Python',
                    '.java': 'Java',
                    '.js': 'Javascript',
                    '.cpp': 'Cpp',
                    '.go': 'Go',
                    '.php': 'Php',
                    '.rb': 'Ruby'
                }
                self.language_combo.set(ext_to_lang.get(file_ext, 'Auto Detect'))
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
        code = self.code_text.get("1.0", "end-1c")
        language = self.language_var.get().lower()

        if not code.strip():
            messagebox.showwarning("Warning", "Please enter some code to summarize.")
            return

        try:
            # If language is 'auto detect' or language names 
            if language == 'auto detect':
                language = LanguageSummarizer.get_language(code)
            
            # Generate summary using the language-agnostic approach
            summary = LanguageSummarizer.summarize_code(code, language)
            
            self.summary_text.configure(state="normal")
            self.summary_text.delete("1.0", "end")
            self.summary_text.insert("end", summary)
            self.summary_text.configure(state="disabled")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
