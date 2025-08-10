#!/usr/bin/env python3
"""
Sample Interactions with the Multilingual Teacher Chatbot

This file demonstrates how to use the chatbot programmatically
for different use cases and languages.
"""

import os
import sys
from dotenv import load_dotenv

# Add the chatbot package to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'chatbot'))

from chatbot import (
    GeminiClient, 
    LanguageDetector, 
    PromptBuilder, 
    SessionManager
)

def setup_chatbot():
    """Set up the chatbot components."""
    load_dotenv()
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key or api_key == 'your_actual_api_key_here':
        print("❌ Please set GEMINI_API_KEY in your .env file")
        return None, None, None, None
    
    try:
        client = GeminiClient(api_key)
        detector = LanguageDetector()
        prompt_builder = PromptBuilder()
        session_manager = SessionManager()
        
        print("✅ Chatbot initialized successfully!")
        return client, detector, prompt_builder, session_manager
        
    except Exception as e:
        print(f"❌ Error initializing chatbot: {e}")
        return None, None, None, None

def example_english_questions():
    """Example English questions and responses."""
    print("\n🇺🇸 English Examples")
    print("=" * 40)
    
    questions = [
        "What is photosynthesis?",
        "Explain the water cycle",
        "How do plants grow?",
        "What is gravity?",
        "Explain the food chain"
    ]
    
    return questions

def example_hindi_questions():
    """Example Hindi questions and responses."""
    print("\n🇮🇳 Hindi Examples")
    print("=" * 40)
    
    questions = [
        "प्रकाश संश्लेषण क्या है?",
        "जल चक्र को समझाइए",
        "पौधे कैसे बढ़ते हैं?",
        "गुरुत्वाकर्षण क्या है?",
        "खाद्य श्रृंखला को समझाइए"
    ]
    
    return questions

def example_telugu_questions():
    """Example Telugu questions and responses."""
    print("\n🇮🇳 Telugu Examples")
    print("=" * 40)
    
    questions = [
        "కిరణజన్య సంయోగ క్రియ అంటే ఏమిటి?",
        "నీటి చక్రాన్ని వివరించండి",
        "మొక్కలు ఎలా పెరుగుతాయి?",
        "గురుత్వాకర్షణ అంటే ఏమిటి?",
        "ఆహార గొలుసును వివరించండి"
    ]
    
    return questions

def run_interactive_demo():
    """Run an interactive demo of the chatbot."""
    print("🌟 Multilingual Teacher Chatbot - Interactive Demo")
    print("=" * 60)
    
    # Set up chatbot
    client, detector, prompt_builder, session_manager = setup_chatbot()
    if not all([client, detector, prompt_builder, session_manager]):
        return
    
    # Create session
    session_id = session_manager.create_session()
    print(f"📝 Session created: {session_id}")
    
    # Language options
    languages = {
        '1': ('en', 'English'),
        '2': ('hi', 'Hindi'),
        '3': ('te', 'Telugu'),
        '4': ('auto', 'Auto-detect')
    }
    
    print("\n🌐 Choose your language:")
    for key, (code, name) in languages.items():
        print(f"  {key}. {name}")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-4) or 'quit' to exit: ").strip()
            
            if choice.lower() in ['quit', 'exit', 'q']:
                break
            
            if choice not in languages:
                print("❌ Invalid choice. Please enter 1-4.")
                continue
            
            lang_code, lang_name = languages[choice]
            
            if lang_code == 'auto':
                print("🎯 Auto-detection mode enabled!")
                print("Type your question in any supported language...")
            else:
                print(f"🌐 Language set to: {lang_name}")
            
            # Get user question
            question = input(f"\n💭 Ask your question: ").strip()
            
            if not question:
                continue
            
            if question.lower() in ['quit', 'exit', 'q']:
                break
            
            # Process the question
            print("🤔 Processing your question...")
            
            # Detect language if auto-mode
            if lang_code == 'auto':
                detected_lang, confidence = detector.detect_language(question)
                print(f"🔍 Detected: {detected_lang} (confidence: {confidence:.2f})")
                final_lang = detected_lang
            else:
                final_lang = lang_code
            
            # Build prompt and get response
            prompt = prompt_builder.build_teacher_prompt(question, final_lang)
            response = client.generate_response(prompt)
            
            # Store in session
            session_manager.add_message(session_id, question, response)
            
            # Display response
            print(f"\n🤖 Teacher Response:")
            print("-" * 40)
            print(response)
            print("-" * 40)
            
        except KeyboardInterrupt:
            print("\n\n👋 Demo ended. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            print("🔄 Please try again.")

def run_batch_demo():
    """Run a batch demo with predefined questions."""
    print("🚀 Multilingual Teacher Chatbot - Batch Demo")
    print("=" * 60)
    
    # Set up chatbot
    client, detector, prompt_builder, session_manager = setup_chatbot()
    if not all([client, detector, prompt_builder, session_manager]):
        return
    
    # Create session
    session_id = session_manager.create_session()
    
    # Get example questions
    en_questions = example_english_questions()
    hi_questions = example_hindi_questions()
    te_questions = example_telugu_questions()
    
    # Process English questions
    print("\n🇺🇸 Processing English questions...")
    for i, question in enumerate(en_questions[:2], 1):  # Limit to 2 for demo
        print(f"\n{i}. Question: {question}")
        try:
            prompt = prompt_builder.build_teacher_prompt(question, 'en')
            response = client.generate_response(prompt)
            print(f"   Response: {response[:100]}...")
            session_manager.add_message(session_id, question, response)
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Process Hindi questions
    print("\n🇮🇳 Processing Hindi questions...")
    for i, question in enumerate(hi_questions[:2], 1):  # Limit to 2 for demo
        print(f"\n{i}. Question: {question}")
        try:
            prompt = prompt_builder.build_teacher_prompt(question, 'hi')
            response = client.generate_response(prompt)
            print(f"   Response: {response[:100]}...")
            session_manager.add_message(session_id, question, response)
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Process Telugu questions
    print("\n🇮🇳 Processing Telugu questions...")
    for i, question in enumerate(te_questions[:2], 1):  # Limit to 2 for demo
        print(f"\n{i}. Question: {question}")
        try:
            prompt = prompt_builder.build_teacher_prompt(question, 'te')
            response = client.generate_response(prompt)
            print(f"   Response: {response[:100]}...")
            session_manager.add_message(session_id, question, response)
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print(f"\n✅ Batch demo completed! Session: {session_id}")
    print(f"📊 Total messages: {len(session_manager.get_session_history(session_id))}")

def main():
    """Main function to run examples."""
    print("🌟 Multilingual Teacher Chatbot Examples")
    print("=" * 50)
    
    print("\nChoose demo mode:")
    print("1. Interactive Demo")
    print("2. Batch Demo")
    print("3. Show Example Questions")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == '1':
        run_interactive_demo()
    elif choice == '2':
        run_batch_demo()
    elif choice == '3':
        print("\n📚 Example Questions by Language:")
        example_english_questions()
        example_hindi_questions()
        example_telugu_questions()
    else:
        print("❌ Invalid choice.")

if __name__ == "__main__":
    main()
