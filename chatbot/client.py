"""
Gemini AI API client wrapper for the multilingual chatbot.

This module provides a clean interface to the Gemini API with
retry logic, error handling, and easy replacement for other LLM providers.
"""

import os
import time
import logging
from typing import Optional, Dict, Any, List
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiClient:
    """
    Client wrapper for Gemini AI API with retry logic and error handling.
    
    This class abstracts the Gemini API calls and can be easily replaced
    with other LLM providers by implementing the same interface.
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-1.5-flash"):
        """
        Initialize the Gemini client.
        
        Args:
            api_key: Gemini API key (defaults to GEMINI_API_KEY env var)
            model: Model name to use (default: gemini-1.5-flash)
        """
        self.api_key = api_key or os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
        self.model_name = model
        self.max_retries = int(os.getenv('MAX_RETRIES', '3'))
        self.retry_delay = 1.0
        
        if not self.api_key:
            raise ValueError(
                "Gemini API key not found. Set GEMINI_API_KEY or GOOGLE_API_KEY "
                "environment variable, or pass api_key parameter."
            )
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        
        # Try to initialize with the specified model, fallback to alternatives if needed
        self.model = self._initialize_model()
        logger.info(f"Gemini client initialized with model: {self.model_name}")
    
    def _initialize_model(self):
        """Initialize the model with fallback options."""
        fallback_models = [
            self.model_name,
            "gemini-1.5-flash",
            "gemini-1.5-pro", 
            "gemini-pro",
            "gemini-1.0-pro"
        ]
        
        for model_name in fallback_models:
            try:
                model = genai.GenerativeModel(
                    model_name=model_name,
                    safety_settings={
                        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                    }
                )
                # Test if model is accessible
                model.generate_content("test")
                self.model_name = model_name  # Update to the working model
                return model
            except Exception as e:
                logger.warning(f"Failed to initialize model {model_name}: {e}")
                continue
        
        # If all models fail, raise an error
        raise Exception(f"Failed to initialize any Gemini model. Tried: {fallback_models}")
    
    def generate_response(
        self, 
        prompt: str, 
        system_message: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generate a response from Gemini API.
        
        Args:
            prompt: User prompt/message
            system_message: Optional system message/instruction
            temperature: Response creativity (0.0-1.0)
            max_tokens: Maximum response length
            
        Returns:
            Generated response text
            
        Raises:
            Exception: If API call fails after retries
        """
        # Build the full prompt
        full_prompt = self._build_full_prompt(prompt, system_message)
        
        # Configure generation parameters
        generation_config = {
            'temperature': temperature,
        }
        if max_tokens:
            generation_config['max_output_tokens'] = max_tokens
        
        # Retry logic with exponential backoff
        last_exception = None
        
        for attempt in range(self.max_retries + 1):
            try:
                response = self.model.generate_content(
                    full_prompt,
                    generation_config=generation_config
                )
                
                if response.text:
                    logger.info(f"Successfully generated response (attempt {attempt + 1})")
                    return response.text.strip()
                else:
                    logger.warning(f"Empty response from Gemini (attempt {attempt + 1})")
                    return "I apologize, but I couldn't generate a proper response. Please try again."
                    
            except Exception as e:
                last_exception = e
                logger.warning(f"API call failed (attempt {attempt + 1}): {e}")
                
                if attempt < self.max_retries:
                    # Exponential backoff
                    delay = self.retry_delay * (2 ** attempt)
                    logger.info(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    logger.error(f"All retry attempts failed. Last error: {e}")
                    break
        
        # If we get here, all retries failed
        error_msg = f"Failed to generate response after {self.max_retries + 1} attempts"
        if last_exception:
            error_msg += f". Last error: {last_exception}"
        
        logger.error(error_msg)
        raise Exception(error_msg)
    
    def _build_full_prompt(self, prompt: str, system_message: Optional[str] = None) -> str:
        """
        Build the full prompt combining system message and user prompt.
        
        Args:
            prompt: User prompt
            system_message: Optional system message
            
        Returns:
            Combined prompt string
        """
        if system_message:
            return f"{system_message}\n\nUser: {prompt}\n\nAssistant:"
        else:
            return f"User: {prompt}\n\nAssistant:"
    
    def test_connection(self) -> bool:
        """
        Test the API connection with a simple prompt.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            test_response = self.generate_response(
                "Hello, please respond with 'Connection successful'",
                temperature=0.1
            )
            return "Connection successful" in test_response
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the current model.
        
        Returns:
            Dictionary with model information
        """
        return {
            'model_name': self.model_name,
            'provider': 'Gemini AI',
            'api_key_configured': bool(self.api_key),
            'max_retries': self.max_retries
        }

# Alternative HTTP-based client for cases where google.generativeai is not available
class GeminiHTTPClient:
    """
    HTTP-based Gemini client as a fallback option.
    
    This class can be used if the official Gemini library is not available
    or if you prefer direct HTTP calls.
    """
    
    def __init__(self, api_key: str, model: str = "gemini-pro"):
        """
        Initialize the HTTP client.
        
        Args:
            api_key: Gemini API key
            model: Model name to use
        """
        self.api_key = api_key
        self.model = model
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"
        self.max_retries = int(os.getenv('MAX_RETRIES', '3'))
        
        if not self.api_key:
            raise ValueError("API key is required for HTTP client")
    
    def generate_response(
        self, 
        prompt: str, 
        system_message: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generate response using HTTP API calls.
        
        This is a placeholder implementation. In a real scenario,
        you would implement the actual HTTP calls to Gemini API.
        
        Args:
            prompt: User prompt
            system_message: Optional system message
            temperature: Response creativity
            max_tokens: Maximum response length
            
        Returns:
            Generated response text
        """
        # TODO: Implement actual HTTP calls to Gemini API
        # This is a stub implementation
        
        import requests
        
        url = f"{self.base_url}/{self.model}:generateContent"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        # Build request payload
        content = []
        if system_message:
            content.append({"role": "user", "parts": [{"text": system_message}]})
        
        content.append({"role": "user", "parts": [{"text": prompt}]})
        
        payload = {
            "contents": content,
            "generationConfig": {
                "temperature": temperature,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": max_tokens or 2048,
            }
        }
        
        # Make API call with retry logic
        for attempt in range(self.max_retries + 1):
            try:
                response = requests.post(url, headers=headers, json=payload, timeout=30)
                response.raise_for_status()
                
                result = response.json()
                if 'candidates' in result and result['candidates']:
                    return result['candidates'][0]['content']['parts'][0]['text'].strip()
                else:
                    return "I apologize, but I couldn't generate a proper response."
                    
            except requests.exceptions.RequestException as e:
                if attempt < self.max_retries:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                else:
                    raise Exception(f"HTTP API call failed: {e}")
        
        raise Exception("All retry attempts failed")

def create_client(api_key: Optional[str] = None, use_http: bool = False) -> GeminiClient:
    """
    Factory function to create a Gemini client.
    
    Args:
        api_key: API key (defaults to environment variable)
        use_http: Whether to use HTTP client instead of official library
        
    Returns:
        Configured client instance
    """
    if use_http:
        return GeminiHTTPClient(api_key or os.getenv('GEMINI_API_KEY'))
    else:
        return GeminiClient(api_key)
