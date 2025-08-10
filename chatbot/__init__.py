from .client import GeminiClient
from .language import LanguageDetector, SUPPORTED_LANGUAGES
from .prompt_builder import PromptBuilder
from .session import SessionManager
from .utils import generate_teacher_response, sanitize_input

__version__ = "1.0.0"
__author__ = "Multilingual Teacher Chatbot Team"

__all__ = [
    "GeminiClient",
    "LanguageDetector", 
    "SUPPORTED_LANGUAGES",
    "PromptBuilder",
    "SessionManager",
    "generate_teacher_response",
    "sanitize_input"
]
