import re
import logging
from typing import Dict, Any, Optional, Tuple
from .client import GeminiClient, create_client
from .language import LanguageDetector, SUPPORTED_LANGUAGES
from .prompt_builder import PromptBuilder
from .session import get_session_manager, create_new_session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def sanitize_input(text: str) -> str:
    if not text:
        return ""
    
    text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)
    
    text = text.replace('`', '\\`')
    text = text.replace('```', '\\`\\`\\`')
    
    max_length = 1000
    if len(text) > max_length:
        text = text[:max_length] + "..."
        logger.warning(f"Input truncated to {max_length} characters")
    
    text = re.sub(r'\s+', ' ', text.strip())
    
    return text

def parse_teacher_response(response_text: str, language_code: str) -> Dict[str, Any]:
    """
    Parse the LLM response into structured components.
    
    Args:
        response_text: Raw response from the LLM
        language_code: Language code for the response
        
    Returns:
        Dictionary with parsed response components
    """
    # Initialize response structure
    parsed_response = {
        'language': language_code,
        'text': response_text,
        'definition': '',
        'examples': [],
        'application': '',
        'raw_response': response_text
    }
    
    # Try to extract structured components based on language
    if language_code == 'en':
        parsed_response.update(_parse_english_response(response_text))
    elif language_code == 'hi':
        parsed_response.update(_parse_hindi_response(response_text))
    elif language_code == 'te':
        parsed_response.update(_parse_telugu_response(response_text))
    else:
        # Fallback parsing for unknown languages
        parsed_response.update(_parse_generic_response(response_text))
    
    return parsed_response

def _parse_english_response(text: str) -> Dict[str, Any]:
    components = {
        'definition': '',
        'examples': [],
        'application': ''
    }
    
    lines = text.split('\n')
    current_section = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Detect sections
        if re.match(r'^\d+\.\s*(Definition|Explanation)', line, re.IGNORECASE):
            current_section = 'definition'
        elif re.match(r'^\d+\.\s*Examples?', line, re.IGNORECASE):
            current_section = 'examples'
        elif re.match(r'^\d+\.\s*Application', line, re.IGNORECASE):
            current_section = 'application'
        elif line.startswith('1.') or line.startswith('2.') or line.startswith('3.'):
            # Skip numbered list markers
            continue
        else:
            # Add content to current section
            if current_section == 'definition':
                components['definition'] += line + ' '
            elif current_section == 'examples':
                if line and not line.startswith('-'):
                    components['examples'].append(line)
            elif current_section == 'application':
                components['application'] += line + ' '
    
    # Clean up
    components['definition'] = components['definition'].strip()
    components['application'] = components['application'].strip()
    components['examples'] = [ex.strip() for ex in components['examples'] if ex.strip()]
    
    return components

def _parse_hindi_response(text: str) -> Dict[str, Any]:
    components = {
        'definition': '',
        'examples': [],
        'application': ''
    }
    
    lines = text.split('\n')
    current_section = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Detect Hindi sections
        if re.search(r'परिभाषा|स्पष्टीकरण', line):
            current_section = 'definition'
        elif re.search(r'उदाहरण', line):
            current_section = 'examples'
        elif re.search(r'अनुप्रयोग|टिप', line):
            current_section = 'application'
        elif line.startswith('1.') or line.startswith('2.') or line.startswith('3.'):
            continue
        else:
            # Add content to current section
            if current_section == 'definition':
                components['definition'] += line + ' '
            elif current_section == 'examples':
                if line and not line.startswith('-'):
                    components['examples'].append(line)
            elif current_section == 'application':
                components['application'] += line + ' '
    
    # Clean up
    components['definition'] = components['definition'].strip()
    components['application'] = components['application'].strip()
    components['examples'] = [ex.strip() for ex in components['examples'] if ex.strip()]
    
    return components

def _parse_telugu_response(text: str) -> Dict[str, Any]:
    components = {
        'definition': '',
        'examples': [],
        'application': ''
    }
    
    lines = text.split('\n')
    current_section = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Detect Telugu sections
        if re.search(r'నిర్వచనం|వివరణ', line):
            current_section = 'definition'
        elif re.search(r'ఉదాహరణ', line):
            current_section = 'examples'
        elif re.search(r'అప్లికేషన్|చిట్కా', line):
            current_section = 'application'
        elif line.startswith('1.') or line.startswith('2.') or line.startswith('3.'):
            continue
        else:
            # Add content to current section
            if current_section == 'definition':
                components['definition'] += line + ' '
            elif current_section == 'examples':
                if line and not line.startswith('-'):
                    components['examples'].append(line)
            elif current_section == 'application':
                components['application'] += line + ' '
    
    # Clean up
    components['definition'] = components['definition'].strip()
    components['application'] = components['application'].strip()
    components['examples'] = [ex.strip() for ex in components['examples'] if ex.strip()]
    
    return components

def _parse_generic_response(text: str) -> Dict[str, Any]:
    """Generic parsing for unknown languages."""
    return {
        'definition': text,
        'examples': [],
        'application': ''
    }

def generate_teacher_response(
    user_text: str, 
    session_id: Optional[str] = None,
    force_language: Optional[str] = None,
    client: Optional[GeminiClient] = None
) -> Dict[str, Any]:
    try:
        # Sanitize input
        sanitized_text = sanitize_input(user_text)
        if not sanitized_text:
            raise ValueError("Empty or invalid input text")
        
        # Initialize components
        language_detector = LanguageDetector()
        prompt_builder = PromptBuilder()
        session_manager = get_session_manager()
        
        # Create or get session
        if not session_id:
            session_id = create_new_session()
        
        # Detect language (or use forced language)
        if force_language and force_language in SUPPORTED_LANGUAGES:
            detected_language = force_language
            confidence = 1.0
        else:
            detected_language, confidence = language_detector.detect_language(sanitized_text)
        
        # Validate detected language
        if detected_language not in SUPPORTED_LANGUAGES:
            # Handle unsupported language
            error_response = _handle_unsupported_language(detected_language, client)
            return {
                'language': 'en',
                'text': error_response,
                'definition': error_response,
                'examples': [],
                'application': '',
                'raw_response': error_response,
                'session_id': session_id,
                'error': 'unsupported_language'
            }
        
        # Get conversation context
        context = session_manager.get_conversation_context(session_id, max_messages=3)
        
        # Build the teacher prompt
        system_prompt = prompt_builder.build_teacher_prompt(
            sanitized_text, 
            detected_language, 
            context
        )
        
        # Initialize client if not provided
        if not client:
            client = create_client()
        
        # Generate response from LLM
        logger.info(f"Generating response for language: {detected_language} (confidence: {confidence:.2f})")
        raw_response = client.generate_response(
            prompt=sanitized_text,
            system_message=system_prompt,
            temperature=0.7
        )
        
        # Parse the response
        parsed_response = parse_teacher_response(raw_response, detected_language)
        parsed_response['session_id'] = session_id
        parsed_response['confidence'] = confidence
        
        # Store messages in session
        session_manager.add_user_message(session_id, sanitized_text, detected_language)
        session_manager.add_assistant_message(session_id, raw_response, detected_language)
        
        logger.info(f"Successfully generated response for session {session_id}")
        return parsed_response
        
    except Exception as e:
        logger.error(f"Error generating teacher response: {e}")
        
        # Return error response
        error_msg = _get_error_message(str(e), detected_language if 'detected_language' in locals() else 'en')
        
        return {
            'language': detected_language if 'detected_language' in locals() else 'en',
            'text': error_msg,
            'definition': error_msg,
            'examples': [],
            'application': '',
            'raw_response': error_msg,
            'session_id': session_id if 'session_id' in locals() else None,
            'error': 'generation_failed',
            'error_details': str(e)
        }

def _handle_unsupported_language(detected_lang: str, client: Optional[GeminiClient]) -> str:
    """Handle unsupported language detection."""
    if not client:
        return (
            "I apologize, but I don't support the language you're using. "
            "I can help you in English, Hindi, and Telugu. "
            "Please try asking your question in one of these languages."
        )
    
    # Try to get a response in English explaining the limitation
    try:
        error_prompt = (
            "The user's message is in a language I don't support. "
            "Please explain in English that I support English, Hindi, and Telugu, "
            "and ask them to try again in one of these languages."
        )
        
        response = client.generate_response(
            prompt=error_prompt,
            temperature=0.3
        )
        return response
    except:
        return (
            "I apologize, but I don't support the language you're using. "
            "I can help you in English, Hindi, and Telugu. "
            "Please try asking your question in one of these languages."
        )

def _get_error_message(error: str, language: str) -> str:
    error_messages = {
        'en': (
            "I apologize, but I encountered an error while processing your request. "
            "Please try again in a moment. If the problem persists, "
            "check your internet connection and try again."
        ),
        'hi': (
            "मैं क्षमा चाहता हूं, लेकिन आपके अनुरोध को संसाधित करने में एक त्रुटि हुई। "
            "कृपया कुछ देर बाद फिर से कोशिश करें। यदि समस्या बनी रहती है, "
            "तो अपना इंटरनेट कनेक्शन जांचें और फिर से कोशिश करें।"
        ),
        'te': (
            "నేను క్షమాపణ కోరుకుంటున్నాను, కానీ మీ అభ్యర్థనను ప్రాసెస్ చేయడంలో ఒక లోపం ఉంది. "
            "దయచేసి కొంత సమయం తర్వాత మళ్లీ ప్రయత్నించండి. సమస్య కొనసాగితే, "
            "మీ ఇంటర్నెట్ కనెక్షన్‌ని తనిఖీ చేసి మళ్లీ ప్రయత్నించండి."
        )
    }
    
    return error_messages.get(language, error_messages['en'])

def format_response_for_display(response: Dict[str, Any]) -> str:
    if 'error' in response:
        return f"Error: {response['text']}"
    
    # Get language-specific formatting
    language = response.get('language', 'en')
    
    if language == 'hi':
        return _format_hindi_response(response)
    elif language == 'te':
        return _format_telugu_response(response)
    else:
        return _format_english_response(response)

def _format_english_response(response: Dict[str, Any]) -> str:
    parts = []
    
    if response.get('definition'):
        parts.append(f"Definition: {response['definition']}")
    
    if response.get('examples'):
        parts.append("Examples:")
        for i, example in enumerate(response['examples'][:2], 1):
            parts.append(f"  {i}. {example}")
    
    if response.get('application'):
        parts.append(f"Application: {response['application']}")
    
    return "\n\n".join(parts)

def _format_hindi_response(response: Dict[str, Any]) -> str:
    """Format Hindi response for display."""
    parts = []
    
    if response.get('definition'):
        parts.append(f"परिभाषा: {response['definition']}")
    
    if response.get('examples'):
        parts.append("उदाहरण:")
        for i, example in enumerate(response['examples'][:2], 1):
            parts.append(f"  {i}. {example}")
    
    if response.get('application'):
        parts.append(f"अनुप्रयोग: {response['application']}")
    
    return "\n\n".join(parts)

def _format_telugu_response(response: Dict[str, Any]) -> str:
    """Format Telugu response for display."""
    parts = []
    
    if response.get('definition'):
        parts.append(f"నిర్వచనం: {response['definition']}")
    
    if response.get('examples'):
        parts.append("ఉదాహరణలు:")
        for i, example in enumerate(response['examples'][:2], 1):
            parts.append(f"  {i}. {example}")
    
    if response.get('application'):
        parts.append(f"అప్లికేషన్: {response['application']}")
    
    return "\n\n".join(parts)