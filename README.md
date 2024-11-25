# ICA (Intelligent Code Assistant)
# Multi-Language Code Summarizer

A Python-based tool that analyzes and summarizes code across different programming languages. The application provides a graphical user interface for easy interaction and generates comprehensive summaries of code structure, functions, and key concepts.

## Features

- Supports multiple programming languages
- Extracts and analyzes:
  - Class definitions
  - Function names and their arguments
  - Import statements
  - Key terms and concepts
- Clean GUI interface with syntax highlighting
- Natural language summaries of code structure

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/ICA.git
cd ICA
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Ensure NLTK data is downloaded (the program will handle this automatically on first run)

## Usage

1. Run the application:
```bash
python main.py
```

2. Using the GUI:
   - Select the programming language from the dropdown menu
   - Paste or type your code in the input text area
   - Click "Generate Summary" to analyze the code
   - View the generated summary in the output text area

## Project Structure

- `main.py`: Main application file containing the GUI and core functionality
- `language_patterns.py`: Contains regex patterns and metadata for supported languages
- `requirements.txt`: List of Python dependencies
- `README.md`: This file

## Dependencies

- customtkinter: GUI framework
- nltk: Natural Language Processing toolkit
- regex: Regular expression operations

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Authors

Amit Kumar, Rakshit Malik, Kumar Tejaswa

## Acknowledgments

- NLTK team for their comprehensive NLP toolkit
- Python tkinter documentation for GUI implementation guidance
