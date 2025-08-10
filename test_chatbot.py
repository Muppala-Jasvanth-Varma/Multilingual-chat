#!/usr/bin/env python3

import os
import sys
from dotenv import load_dotenv

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'chatbot'))

def test_imports():
    print("🔍 Testing imports...")

    try:
        from chatbot import (
            GeminiClient,
            LanguageDetector,
            PromptBuilder,
            SessionManager,
            SUPPORTED_LANGUAGES
        )
        print("✅ All imports successful!")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_language_detection():
    print("\n🌐 Testing language detection...")

    try:
        from chatbot import LanguageDetector

        detector = LanguageDetector()

        text_en = "What is photosynthesis?"
        lang_en, confidence_en = detector.detect_language(text_en)
        print(f"✅ English: '{text_en}' -> {lang_en} (confidence: {confidence_en:.2f})")

        text_hi = "प्रकाश संश्लेषण क्या है?"
        lang_hi, confidence_hi = detector.detect_language(text_hi)
        print(f"✅ Hindi: '{text_hi}' -> {lang_hi} (confidence: {confidence_hi:.2f})")

        text_te = "కిరణజన్య సంయోగ క్రియ అంటే ఏమిటి?"
        lang_te, confidence_te = detector.detect_language(text_te)
        print(f"✅ Telugu: '{text_te}' -> {lang_te} (confidence: {confidence_te:.2f})")

        return True

    except Exception as e:
        print(f"❌ Language detection error: {e}")
        return False

def test_prompt_builder():
    print("\n📝 Testing prompt builder...")

    try:
        from chatbot import PromptBuilder

        builder = PromptBuilder()

        prompt_en = builder.build_teacher_prompt("What is photosynthesis?", "en")
        print(f"✅ English prompt created ({len(prompt_en)} characters)")

        prompt_hi = builder.build_teacher_prompt("प्रकाश संश्लेषण क्या है?", "hi")
        print(f"✅ Hindi prompt created ({len(prompt_hi)} characters)")

        prompt_te = builder.build_teacher_prompt("కిరణజన్య సంయోగ క్రియ అంటే ఏమిటి?", "te")
        print(f"✅ Telugu prompt created ({len(prompt_te)} characters)")

        return True

    except Exception as e:
        print(f"❌ Prompt builder error: {e}")
        return False

def test_session_manager():
    print("\n💾 Testing session manager...")

    try:
        from chatbot import SessionManager

        manager = SessionManager()

        session_id = manager.create_session()
        print(f"✅ Session created: {session_id}")

        manager.add_user_message(session_id, "Hello", "en")
        manager.add_assistant_message(session_id, "Hi there!", "en")
        manager.add_user_message(session_id, "How are you?", "en")
        manager.add_assistant_message(session_id, "I'm doing well, thank you!", "en")

        context = manager.get_conversation_context(session_id)
        print(f"✅ Session context: {len(context)} messages")

        info = manager.get_session_info(session_id)
        print(f"✅ Session info: {info['total_messages']} total messages")

        manager.end_session(session_id)
        print("✅ Session ended")

        return True

    except Exception as e:
        print(f"❌ Session manager error: {e}")
        return False

def test_gemini_client():
    print("\n🤖 Testing Gemini client...")

    load_dotenv()
    api_key = os.getenv('GEMINI_API_KEY')

    if not api_key or api_key == 'your_actual_api_key_here':
        print("⚠️  No valid API key found. Skipping Gemini client test.")
        print("   Please set GEMINI_API_KEY in your .env file")
        return True

    try:
        from chatbot import GeminiClient

        client = GeminiClient(api_key)

        test_prompt = "Say 'Hello, world!' in exactly 3 words."
        response = client.generate_response(test_prompt)

        if response and len(response.strip()) > 0:
            print(f"✅ Gemini client working! Response: '{response.strip()}'")
            return True
        else:
            print("❌ Gemini client returned empty response")
            return False

    except Exception as e:
        print(f"❌ Gemini client error: {e}")
        return False

def test_utils():
    print("\n🔧 Testing utility functions...")

    try:
        from chatbot import sanitize_input, generate_teacher_response

        test_input = "Hello, world! <script>alert('xss')</script>"
        sanitized = sanitize_input(test_input)
        print(f"✅ Input sanitization: '{test_input}' -> '{sanitized}'")

        mock_response = generate_teacher_response("test", "en")
        print(f"✅ Teacher response generation: {len(mock_response)} characters")

        return True

    except Exception as e:
        print(f"❌ Utils error: {e}")
        return False

def main():
    print("🚀 Starting Multilingual Teacher Chatbot Tests")
    print("=" * 50)

    tests = [
        ("Imports", test_imports),
        ("Language Detection", test_language_detection),
        ("Prompt Builder", test_prompt_builder),
        ("Session Manager", test_session_manager),
        ("Gemini Client", test_gemini_client),
        ("Utilities", test_utils),
    ]

    results = []

    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))

    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)

    passed = 0
    total = len(results)

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:20} {status}")
        if result:
            passed += 1

    print(f"\nOverall: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! Your chatbot is ready to use.")
        print("\nNext steps:")
        print("1. Set your GEMINI_API_KEY in .env file")
        print("2. Run CLI: python main.py")
        print("3. Run Web UI: streamlit run streamlit_app.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())
