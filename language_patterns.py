# language_patterns.py

LANGUAGE_PATTERNS = {
    'python': {
        'class': r'class\s+(\w+)',
        'function': r'def\s+(\w+)\s*\([^)]*\)',
        'import': r'(?:from\s+[\w.]+\s+)?import\s+[\w,\s]+',
        'arguments': r'def\s+\w+\s*\((.*?)\)',
        'module_used': ['ast', 'tkinter', 'nltk', 're'],
        'comment_single': r'#.*',
        'comment_multi': r'"""[\s\S]*?"""',
        'module_purposes': {
            'ast': 'parse and analyze the structure of Python code',
            'tkinter': 'create an interactive graphical user interface',
            'nltk': 'perform Natural Language Processing for text analysis',
            're': 'handle regular expressions and pattern matching'
        }
    },
    'java': {
        'class': r'class\s+(\w+)',
        'function': r'(?:public|private|protected)?\s*(?:static\s+)?[\w<>[\],\s]+\s+(\w+)\s*\([^)]*\)',
        'import': r'import\s+[\w.]+(?:\s*\*)?;',
        'arguments': r'(?:public|private|protected)?\s*(?:static\s+)?[\w<>[\],\s]+\s+\w+\s*\((.*?)\)',
        'module_used': ['java.util', 'java.io', 'javax.swing'],
        'comment_single': r'\/\/.*',
        'comment_multi': r'\/\*[\s\S]*?\*\/',
        'module_purposes': {
            'java.util': 'provide essential utility classes',
            'java.io': 'handle input/output operations',
            'javax.swing': 'create graphical user interfaces'
        }
    },
    'javascript': {
        'class': r'class\s+(\w+)',
        'function': r'(?:function\s+(\w+)|const\s+(\w+)\s*=\s*(?:async\s*)?(?:\(.*?\)|[^=>]*)\s*=>)',
        'import': r'(?:import\s+.*?from\s+[\'"].*?[\'"]|require\s*\([\'"].*?[\'"]\))',
        'arguments': r'function\s+\w+\s*\((.*?)\)|const\s+\w+\s*=\s*\((.*?)\)\s*=>',
        'module_used': ['react', 'express', 'node'],
        'comment_single': r'\/\/.*',
        'comment_multi': r'\/\*[\s\S]*?\*\/',
        'module_purposes': {
            'react': 'build user interfaces',
            'express': 'create web applications and APIs',
            'node': 'execute JavaScript server-side'
        }
    },
    'cpp': {
        'class': r'class\s+(\w+)',
        'function': r'(?:[\w\*&]+\s+)?(\w+)\s*\([^)]*\)\s*(?:const)?\s*(?:{|;)',
        'import': r'#include\s*[<"][\w.]+[>"]',
        'arguments': r'(?:[\w\*&]+\s+)?\w+\s*\((.*?)\)',
        'module_used': ['iostream', 'string', 'vector'],
        'comment_single': r'\/\/.*',
        'comment_multi': r'\/\*[\s\S]*?\*\/',
        'module_purposes': {
            'iostream': 'handle input/output operations',
            'string': 'work with text strings',
            'vector': 'manage dynamic arrays'
        }
    },
    'go': {
        'class': r'type\s+(\w+)\s+struct',
        'function': r'func\s+(?:\(\w+\s+\*?\w+\)\s+)?(\w+)\s*\([^)]*\)',
        'import': r'import\s+(?:\([^)]*\)|"[^"]*")',
        'arguments': r'func\s+(?:\(\w+\s+\*?\w+\)\s+)?\w+\s*\((.*?)\)',
        'module_used': ['fmt', 'net/http', 'encoding/json'],
        'comment_single': r'\/\/.*',
        'comment_multi': r'\/\*[\s\S]*?\*\/',
        'module_purposes': {
            'fmt': 'format and print text',
            'net/http': 'create HTTP servers and clients',
            'encoding/json': 'work with JSON data'
        }
    },
    'php': {
        'class': r'class\s+(\w+)',
        'function': r'function\s+(\w+)\s*\([^)]*\)',
        'import': r'(?:require|include|require_once|include_once)\s*(?:\([\'"].*?[\'"]\)|[\'"].*?[\'"])',
        'arguments': r'function\s+\w+\s*\((.*?)\)',
        'module_used': ['PDO', 'mysqli', 'Laravel'],
        'comment_single': r'(?:\/\/|#).*',
        'comment_multi': r'\/\*[\s\S]*?\*\/',
        'module_purposes': {
            'PDO': 'handle database operations',
            'mysqli': 'work with MySQL databases',
            'Laravel': 'build web applications'
        }
    },
    'ruby': {
        'class': r'class\s+(\w+)',
        'function': r'def\s+(\w+)',
        'import': r'(?:require|include)\s+[\'"].*?[\'"]',
        'arguments': r'def\s+\w+(?:\((.*?)\))?',
        'module_used': ['rails', 'sinatra', 'active_record'],
        'comment_single': r'#.*',
        'comment_multi': r'=begin[\s\S]*?=end',
        'module_purposes': {
            'rails': 'build web applications',
            'sinatra': 'create web services',
            'active_record': 'work with databases'
        }
    }
}

def get_supported_languages():
    """Return a list of supported programming languages."""
    return list(LANGUAGE_PATTERNS.keys())

def get_language_patterns(language):
    """Get patterns for a specific language."""
    return LANGUAGE_PATTERNS.get(language.lower())