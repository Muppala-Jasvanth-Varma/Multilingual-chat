from typing import Optional, Tuple, Dict, Any
from langdetect import detect, DetectorFactory, LangDetectException
import re

DetectorFactory.seed = 0

SUPPORTED_LANGUAGES = {
    'en': 'English',
    'hi': 'Hindi', 
    'te': 'Telugu'
}

LANG_CONFIDENCE_THRESHOLD = 0.8

class LanguageDetector:
    def __init__(self, confidence_threshold: float = LANG_CONFIDENCE_THRESHOLD):
        self.confidence_threshold = confidence_threshold
        self._supported_codes = set(SUPPORTED_LANGUAGES.keys())
    
    def detect_language(self, text: str) -> Tuple[str, float]:
        if not text or not text.strip():
            return 'en', 0.0
            
        cleaned_text = self._clean_text(text)
        
        try:
            detected_lang = detect(cleaned_text)
            confidence = self._calculate_confidence(cleaned_text, detected_lang)
            
            if detected_lang in self._supported_codes:
                return detected_lang, confidence
            else:
                return 'en', 0.5
                
        except LangDetectException:
            return 'en', 0.3
    
    def is_supported(self, language_code: str) -> bool:
        return language_code in self._supported_codes
    
    def get_language_name(self, language_code: str) -> str:
        return SUPPORTED_LANGUAGES.get(language_code, 'Unknown')
    
    def validate_language(self, language_code: str) -> str:
        if language_code in self._supported_codes:
            return language_code
        return 'en'
    
    def _clean_text(self, text: str) -> str:
        if not text:
            return ""
        
        cleaned = re.sub(r'\s+', ' ', text.strip())
        
        cleaned = re.sub(r'[^\w\s\u0900-\u097F\u0C00-\u0C7F]', '', cleaned)
        
        return cleaned
    
    def _calculate_confidence(self, text: str, detected_lang: str) -> float:
        if detected_lang == 'hi':
            devanagari_chars = len(re.findall(r'[\u0900-\u097F]', text))
            if devanagari_chars > 0:
                return min(0.9, 0.5 + (devanagari_chars / len(text)) * 0.4)
        
        elif detected_lang == 'te':
            telugu_chars = len(re.findall(r'[\u0900-\u0C7F]', text))
            if telugu_chars > 0:
                return min(0.9, 0.5 + (telugu_chars / len(text)) * 0.4)
        
        elif detected_lang == 'en':
            latin_chars = len(re.findall(r'[a-zA-Z]', text))
            if latin_chars > 0:
                return min(0.9, 0.5 + (latin_chars / len(text)) * 0.4)
        
        return 0.6

def detect_language_simple(text: str) -> str:
    detector = LanguageDetector()
    lang_code, _ = detector.detect_language(text)
    return lang_code

def is_hindi_text(text: str) -> bool:
    return bool(re.search(r'[\u0900-\u097F]', text))

def is_telugu_text(text: str) -> bool:
    return bool(re.search(r'[\u0C00-\u0C7F]', text))

def is_english_text(text: str) -> bool:
    latin_chars = len(re.findall(r'[a-zA-Z]', text))
    total_chars = len(re.sub(r'\s', '', text))
    
    if total_chars == 0:
        return True
    
    return (latin_chars / total_chars) > 0.7
