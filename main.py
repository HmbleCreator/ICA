import tkinter as tk
from tkinter import scrolledtext, ttk
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from language_patterns import get_supported_languages, get_language_patterns

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

def extract_function_details(code, patterns):
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

def extract_code_structure(code, language):
    """Extract the structure of the code based on language patterns."""
    patterns = get_language_patterns(language)
    if not patterns:
        return f"Unsupported language: {language}"

    # Clean comments first
    code_clean = re.sub(patterns['comment_multi'], '', code)
    code_clean = re.sub(patterns['comment_single'], '', code_clean)

    structure = {
        'classes': re.findall(patterns['class'], code_clean),
        'functions': extract_function_details(code, patterns),
        'imports': re.findall(patterns['import'], code_clean),
        'modules': patterns['module_used'],
        'module_purposes': patterns['module_purposes']
    }
    
    return structure

def preprocess_code(code, language):
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

def extract_key_terms(tokens, n=5):
    """Extract the most common terms from the code."""
    freq_dist = nltk.FreqDist(tokens)
    return [term for term, _ in freq_dist.most_common(n)]

def summarize_code(code, language):
    """Generate a comprehensive summary of the code."""
    structure = extract_code_structure(code, language)
    
    if isinstance(structure, str):  # Error message
        return structure

    tokens = preprocess_code(code, language)
    key_terms = extract_key_terms(tokens)

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

class CodeSummarizerGUI:
    def __init__(self, master):
        self.master = master
        master.title("Multi-Language Code Summarizer")

        # Language selection
        self.language_label = tk.Label(master, text="Select Programming Language:")
        self.language_label.pack()

        supported_languages = get_supported_languages()
        self.language_var = tk.StringVar()
        self.language_combo = ttk.Combobox(master, 
                                         textvariable=self.language_var,
                                         values=[lang.capitalize() for lang in supported_languages])
        self.language_combo.set(supported_languages[0].capitalize())
        self.language_combo.pack()

        self.code_label = tk.Label(master, text="Enter your code:")
        self.code_label.pack()

        self.code_text = scrolledtext.ScrolledText(master, height=20, width=80)
        self.code_text.pack()

        self.summarize_button = tk.Button(master, text="Generate Summary", command=self.summarize)
        self.summarize_button.pack()

        self.summary_label = tk.Label(master, text="Code Summary:")
        self.summary_label.pack()

        self.summary_text = tk.Text(master, height=10, width=80, wrap=tk.WORD)
        self.summary_text.pack()

    def summarize(self):
        code = self.code_text.get("1.0", tk.END)
        language = self.language_var.get().lower()
        summary = summarize_code(code, language)
        self.summary_text.delete("1.0", tk.END)
        self.summary_text.insert(tk.END, summary)

def main():
    root = tk.Tk()
    app = CodeSummarizerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
