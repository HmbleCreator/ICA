import customtkinter as ctk
from tkinter import messagebox, filedialog
import re
import os
import ast
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from typing import List, Dict, Any

class CodeAnalyzer:
    @staticmethod
    def analyze_function(func_node: ast.FunctionDef) -> Dict[str, Any]:
        """
        Analyze a function's structure and details.
        
        Args:
            func_node (ast.FunctionDef): AST node representing a function
        
        Returns:
            Dict containing function details
        """
        function_details = {
            'name': func_node.name,
            'args': [arg.arg for arg in func_node.args.args],
            'docstring': ast.get_docstring(func_node) or '',
            'line_count': len(func_node.body)
        }
        
        return function_details

    @staticmethod
    def infer_function_description(func_name: str, func_body: List[ast.AST]) -> str:
        """
        Attempt to infer function purpose based on name and body.
        
        Args:
            func_name (str): Name of the function
            func_body (List[ast.AST]): Function body AST nodes
        
        Returns:
            str: Inferred function description
        """
        # Basic heuristics for function purpose inference
        purpose_hints = {
            'extract': 'extracts or retrieves data',
            'process': 'processes or transforms data',
            'calculate': 'performs calculations',
            'generate': 'generates or creates content',
            'validate': 'checks or validates input',
            'parse': 'parses or interprets data',
            'convert': 'converts between different formats',
            'load': 'loads resources or data',
            'save': 'saves or stores data'
        }
        
        # Check function name for purpose hints
        for hint, description in purpose_hints.items():
            if hint in func_name.lower():
                return f"A function that {description}"
        
        return "Purpose could not be automatically inferred"

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

        self.language_var = ctk.StringVar(value="Python")
        self.language_combo = ctk.CTkComboBox(
            self.top_frame, 
            values=["Python", "JavaScript", "Java"],
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
                    ("Python Files", "*.py"),
                    ("All Files", "*.*")
                ]
            )
            
            if file_path:
                with open(file_path, 'r') as file:
                    code_contents = file.read()
                
                self.code_text.delete("1.0", "end")
                self.code_text.insert("1.0", code_contents)
                
                # Set language based on file extension
                file_ext = os.path.splitext(file_path)[1].lower()
                if file_ext == '.py':
                    self.language_combo.set("Python")
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
            if language == 'python':
                summary = self.summarize_python_code(code)
            else:
                summary = f"Summarization for {language} is not yet supported."
            
            self.summary_text.configure(state="normal")
            self.summary_text.delete("1.0", "end")
            self.summary_text.insert("end", summary)
            self.summary_text.configure(state="disabled")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def summarize_python_code(self, code: str) -> str:
        """
        Generate a comprehensive summary of Python code.
        
        Args:
            code (str): Python source code to analyze
        
        Returns:
            str: Detailed code summary
        """
        try:
            # Parse the code into an AST
            tree = ast.parse(code)
            
            # Analyze code structure
            functions = []
            classes = []
            imports = []
            
            # Traverse the AST
            for node in ast.walk(tree):
                # Collect function details
                if isinstance(node, ast.FunctionDef):
                    func_details = CodeAnalyzer.analyze_function(node)
                    func_details['description'] = CodeAnalyzer.infer_function_description(
                        func_details['name'], 
                        node.body
                    )
                    functions.append(func_details)
                
                # Collect class details
                elif isinstance(node, ast.ClassDef):
                    classes.append(node.name)
                
                # Collect import details
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    if isinstance(node, ast.Import):
                        imports.extend([alias.name for alias in node.names])
                    else:
                        imports.append(node.module)
            
            # Prepare summary sections
            summary_parts = [
                "This code implements a Python application.",
                f"It defines {len(classes)} class(es) and {len(functions)} function(s)."
            ]
            
            # Class summary
            if classes:
                summary_parts.append(f"Classes defined: {', '.join(classes)}")
            
            # Function details
            if functions:
                summary_parts.append("Key functions:")
                for func in functions:
                    args_str = ', '.join(func['args']) if func['args'] else 'no arguments'
                    summary_parts.append(
                        f"- '{func['name']}' takes {len(func['args'])} argument(s) ({args_str}). "
                        f"{func['description']}."
                    )
            
            # Import summary
            if imports:
                summary_parts.append(f"Libraries used: {', '.join(set(imports))}")
            
            # Key terms extraction
            tokens = [word for word in re.findall(r'\b\w+\b', code.lower()) 
                      if word not in set(stopwords.words('english'))]
            freq_dist = nltk.FreqDist(tokens)
            key_terms = [term for term, _ in freq_dist.most_common(5)]
            summary_parts.append(f"Key concepts include: {', '.join(key_terms)}")
            
            return " ".join(summary_parts)
        
        except SyntaxError as e:
            return f"Syntax Error: {str(e)}"
        except Exception as e:
            return f"Analysis Error: {str(e)}"
