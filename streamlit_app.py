#!/usr/bin/env python3

import os
import sys
import streamlit as st
from typing import List, Tuple
from dotenv import load_dotenv

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'chatbot'))

from chatbot import (
    GeminiClient, 
    LanguageDetector, 
    PromptBuilder, 
    SessionManager,
    SUPPORTED_LANGUAGES
)

load_dotenv()

st.set_page_config(
    page_title="Multilingual Teacher Chatbot",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.8rem;
        font-weight: bold;
        margin-bottom: 1.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .language-badge {
        background: linear-gradient(45deg, #ff6b6b, #ee5a24);
        color: white;
        padding: 0.4rem 0.8rem;
        border-radius: 1rem;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        margin-left: 0.5rem;
        box-shadow: 0 2px 8px rgba(255, 107, 107, 0.3);
        transition: all 0.3s ease;
    }
    
    .language-badge:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(255, 107, 107, 0.4);
    }
    
    .chat-message {
        padding: 1.2rem;
        border-radius: 1rem;
        margin: 0.8rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .chat-message:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-left: 5px solid #4CAF50;
        margin-left: 2rem;
        position: relative;
    }
    
    .user-message::before {
        content: "👤";
        position: absolute;
        left: -2.5rem;
        top: 50%;
        transform: translateY(-50%);
        font-size: 1.5rem;
        background: #4CAF50;
        border-radius: 50%;
        width: 2rem;
        height: 2rem;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 8px rgba(76, 175, 80, 0.3);
    }
    
    .bot-message {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        color: white;
        border-left: 5px solid #FF9800;
        margin-right: 2rem;
        position: relative;
    }
    
    .bot-message::before {
        content: "🤖";
        position: absolute;
        right: -2.5rem;
        top: 50%;
        transform: translateY(-50%);
        font-size: 1.5rem;
        background: #FF9800;
        border-radius: 50%;
        width: 2rem;
        height: 2rem;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 8px rgba(255, 152, 0, 0.3);
    }
    
    .sidebar-section {
        margin-bottom: 2rem;
        padding: 1rem;
        background: rgba(255,255,255,0.1);
        border-radius: 0.8rem;
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .error-message {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
        color: #d32f2f;
        padding: 1.2rem;
        border-radius: 1rem;
        border-left: 5px solid #f44336;
        box-shadow: 0 4px 12px rgba(244, 67, 54, 0.2);
        font-weight: 600;
    }
    
    .success-message {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        color: #2e7d32;
        padding: 1.2rem;
        border-radius: 1rem;
        border-left: 5px solid #4caf50;
        box-shadow: 0 4px 12px rgba(76, 175, 80, 0.2);
        font-weight: 600;
    }
    
    .stChatInput {
        border-radius: 1.5rem !important;
        border: 2px solid #667eea !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2) !important;
    }
    
    .stChatInput:focus {
        border-color: #764ba2 !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3) !important;
    }
    
    .stButton > button {
        border-radius: 1rem !important;
        background: linear-gradient(45deg, #667eea, #764ba2) !important;
        color: white !important;
        border: none !important;
        padding: 0.5rem 1.5rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
    }
    
    .stSelectbox > div > div {
        border-radius: 0.8rem !important;
        border: 2px solid #667eea !important;
    }
    
    .css-1d391kg {
        background: linear-gradient(180deg, #f093fb 0%, #f5576c 100%);
    }
    
    .main .block-container {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
        border-radius: 1rem;
        margin: 1rem;
    }
    
    .typing-indicator {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 1rem;
        background: rgba(255,255,255,0.9);
        border-radius: 1rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .typing-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #667eea;
        animation: typing 1.4s infinite ease-in-out;
    }
    
    .typing-dot:nth-child(1) { animation-delay: -0.32s; }
    .typing-dot:nth-child(2) { animation-delay: -0.16s; }
    
    @keyframes typing {
        0%, 80%, 100% { transform: scale(0.8); opacity: 0.5; }
        40% { transform: scale(1); opacity: 1; }
    }
    
    @media (max-width: 768px) {
        .main-header { font-size: 2rem; }
        .chat-message { margin: 0.5rem 0; }
        .user-message, .bot-message { margin-left: 1rem; margin-right: 1rem; }
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    if 'chatbot_initialized' not in st.session_state:
        st.session_state.chatbot_initialized = False
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    if 'current_language' not in st.session_state:
        st.session_state.current_language = 'Auto'
    
    if 'session_id' not in st.session_state:
        st.session_state.session_id = None
    
    if 'error_message' not in st.session_state:
        st.session_state.error_message = None

def initialize_chatbot():
    """Initialize the chatbot components."""
    try:
        # Check for API key in multiple sources
        api_key = os.getenv('GEMINI_API_KEY')
        
        # If not in environment, check Streamlit secrets
        if not api_key and hasattr(st, 'secrets'):
            api_key = st.secrets.get('GEMINI_API_KEY')
        
        if not api_key:
            st.error("❌ GEMINI_API_KEY not found.")
            st.info("""
            **For Local Development:** Create a `.env` file with your Gemini API key.
            
            **For Streamlit Cloud:** Go to your app settings → Secrets and add:
            ```
            GEMINI_API_KEY = "your_api_key_here"
            ```
            """)
            return None, None, None, None
        
        client = GeminiClient(api_key)
        detector = LanguageDetector()
        prompt_builder = PromptBuilder()
        session_manager = SessionManager()
        
        st.session_state.chatbot_initialized = True
        return client, detector, prompt_builder, session_manager
        
    except Exception as e:
        st.error(f"❌ Error initializing chatbot: {e}")
        return None, None, None, None

def display_header():
    st.markdown('<h1 class="main-header">🌟 Multilingual Teacher Chatbot</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <p style="font-size: 1.2rem; color: #666;">
                Ask questions in <strong>English</strong>, <strong>हिंदी</strong>, or <strong>తెలుగు</strong><br>
                Get teacher-style responses with definitions, examples, and applications
            </p>
        </div>
        """, unsafe_allow_html=True)

def display_sidebar():
    st.sidebar.title("🎛️ Controls")
    
    st.sidebar.markdown("### 🌐 Language Settings")
    language_mode = st.sidebar.selectbox(
        "Language Mode",
        ["Auto-detect", "English", "Hindi", "Telugu"],
        index=0
    )
    
    if language_mode != "Auto-detect":
        language_code = {"English": "en", "Hindi": "hi", "Telugu": "te"}[language_mode]
        st.session_state.current_language = language_code
    else:
        st.session_state.current_language = "Auto"
    
    st.sidebar.markdown("### 📚 Session Management")
    if st.sidebar.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = []
        if st.session_state.session_id:
            st.session_state.session_id = None
        st.rerun()
    
    st.sidebar.markdown("### ℹ️ Information")
    st.sidebar.markdown("""
    **Supported Languages:**
    - 🇺🇸 English (en)
    - 🇮🇳 Hindi (hi)
    - 🇮🇳 Telugu (te)
    
    **Features:**
    - 🎯 Automatic language detection
    - 📖 Teacher-style responses
    - 💬 Conversation history
    - 🔄 Session management
    """)
    
    st.sidebar.markdown("### 🔌 API Status")
    if st.session_state.chatbot_initialized:
        st.sidebar.success("✅ Connected")
    else:
        st.sidebar.error("❌ Disconnected")
        st.sidebar.info("""
        **Setup Required:**
        1. Get your Gemini API key from [Google AI Studio](https://aistudio.google.com/)
        2. Add it to Streamlit Cloud secrets
        """)

def display_chat_interface():
    st.markdown("### 💬 Chat Interface")
    
    user_input = st.chat_input("Ask your question here...")
    
    if user_input:
        process_user_input(user_input)
        st.rerun()

def process_user_input(user_input: str):
    if not st.session_state.chatbot_initialized:
        st.error("❌ Chatbot not initialized. Please check your API key.")
        return
    
    try:
        client, detector, prompt_builder, session_manager = get_chatbot_components()
        if not all([client, detector, prompt_builder, session_manager]):
            return
        
        if not st.session_state.session_id:
            st.session_state.session_id = session_manager.create_session()
        
        if st.session_state.current_language == "Auto":
            detected_lang, confidence = detector.detect_language(user_input)
            language_name = SUPPORTED_LANGUAGES.get(detected_lang, detected_lang)
        else:
            detected_lang = st.session_state.current_language
            language_name = SUPPORTED_LANGUAGES.get(detected_lang, detected_lang)
            confidence = 1.0
        
        if detected_lang not in SUPPORTED_LANGUAGES:
            st.warning(f"⚠️ Unsupported language detected: {detected_lang}")
            detected_lang = 'en'
            language_name = "English"
        
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input,
            "language": detected_lang,
            "language_name": language_name
        })
        
        with st.spinner(f"🤔 Processing your question in {language_name}..."):
            prompt = prompt_builder.build_teacher_prompt(user_input, detected_lang)
            response = client.generate_response(prompt)
            
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": response,
                "language": detected_lang,
                "language_name": language_name
            })
            
            session_manager.add_message(st.session_state.session_id, user_input, response)
        
        st.session_state.error_message = None
        
    except Exception as e:
        st.error(f"❌ Error processing your question: {e}")
        st.session_state.error_message = str(e)

def get_chatbot_components():
    if not st.session_state.chatbot_initialized:
        return initialize_chatbot()
    
    return initialize_chatbot()

def display_chat_history():
    if not st.session_state.chat_history:
        st.info("💡 Start a conversation by asking a question!")
        return
    
    st.markdown("### 📜 Conversation History")
    
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                <strong>👤 You ({message['language_name']}):</strong><br>
                {message['content']}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message bot-message">
                <strong>🤖 Teacher ({message['language_name']}):</strong><br>
                {message['content']}
            </div>
            """, unsafe_allow_html=True)

def display_error_messages():
    if st.session_state.error_message:
        st.markdown(f"""
        <div class="error-message">
            <strong>❌ Error:</strong> {st.session_state.error_message}
        </div>
        """, unsafe_allow_html=True)

def main():
    initialize_session_state()
    
    display_header()
    
    if not st.session_state.chatbot_initialized:
        client, detector, prompt_builder, session_manager = initialize_chatbot()
        if not all([client, detector, prompt_builder, session_manager]):
            st.error("❌ Failed to initialize chatbot. Please check your configuration.")
            st.stop()
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        display_sidebar()
    
    with col2:
        display_error_messages()
        
        display_chat_interface()
        
        display_chat_history()

if __name__ == "__main__":
    main()
