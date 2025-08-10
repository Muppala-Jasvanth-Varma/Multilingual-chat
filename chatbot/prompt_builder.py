from typing import Dict, List, Optional
from .language import SUPPORTED_LANGUAGES

class PromptBuilder:
    def __init__(self):
        self.system_templates = self._build_system_templates()
        self.response_formats = self._build_response_formats()
    
    def build_teacher_prompt(
        self, 
        user_input: str, 
        language_code: str,
        session_context: Optional[List[str]] = None
    ) -> str:
        if language_code not in SUPPORTED_LANGUAGES:
            language_code = 'en'
        
        system_template = self.system_templates[language_code]
        response_format = self.response_formats[language_code]
        
        prompt_parts = [system_template]
        
        if session_context:
            context_text = self._format_context(session_context, language_code)
            prompt_parts.append(context_text)
        
        prompt_parts.append(response_format)
        
        prompt_parts.append(f"\nUser Question: {user_input}")
        
        prompt_parts.append(self._get_final_instruction(language_code))
        
        return "\n\n".join(prompt_parts)
    
    def _build_system_templates(self) -> Dict[str, str]:
        """Build language-specific system message templates."""
        return {
            'en': (
                "You are a knowledgeable and patient teacher who responds to questions "
                "in a clear, educational manner. Always respond in the same language "
                "as the user's question. Provide helpful, accurate information that "
                "helps students understand the topic better."
            ),
            'hi': (
                "आप एक जानकार और धैर्यवान शिक्षक हैं जो प्रश्नों का उत्तर "
                "स्पष्ट और शैक्षिक तरीके से देते हैं। हमेशा उसी भाषा में "
                "जवाब दें जिस भाषा में उपयोगकर्ता ने प्रश्न पूछा है। "
                "छात्रों को विषय को बेहतर ढंग से समझने में मदद करने वाली "
                "सहायक और सटीक जानकारी प्रदान करें।"
            ),
            'te': (
                "మీరు ప్రశ్నలకు స్పష్టమైన మరియు విద్యాపరమైన పద్ధతిలో "
                "సమాధానం ఇచ్చే జ్ఞానవంతుడు మరియు ఓపికైన ఉపాధ్యాయుడు. "
                "ఎల్లప్పుడూ వినియోగదారు ప్రశ్న అడిగిన భాషలోనే సమాధానం ఇవ్వండి. "
                "విద్యార్థులకు విషయాన్ని మెరుగ్గా అర్థం చేసుకోవడానికి సహాయపడే "
                "సహాయకరమైన మరియు ఖచ్చితమైన సమాచారాన్ని అందించండి."
            )
        }
    
    def _build_response_formats(self) -> Dict[str, str]:
        """Build language-specific response format instructions."""
        return {
            'en': (
                "Please structure your response in the following format:\n"
                "1. Definition/Explanation: Provide a clear, concise definition or explanation (1-3 sentences)\n"
                "2. Examples: Give 2 relevant, illustrative examples\n"
                "3. Application: Provide a brief practical application or tip (1-2 sentences)\n\n"
                "Keep your response focused, educational, and helpful."
            ),
            'hi': (
                "कृपया अपना उत्तर निम्नलिखित प्रारूप में संरचित करें:\n"
                "1. परिभाषा/स्पष्टीकरण: एक स्पष्ट, संक्षिप्त परिभाषा या स्पष्टीकरण प्रदान करें (1-3 वाक्य)\n"
                "2. उदाहरण: 2 प्रासंगिक, उदाहरणात्मक उदाहरण दें\n"
                "3. अनुप्रयोग: एक संक्षिप्त व्यावहारिक अनुप्रयोग या टिप प्रदान करें (1-2 वाक्य)\n\n"
                "अपना उत्तर केंद्रित, शैक्षिक और सहायक रखें।"
            ),
            'te': (
                "దయచేసి మీ సమాధానాన్ని క్రింది ఫార్మాట్‌లో నిర్మించండి:\n"
                "1. నిర్వచనం/వివరణ: స్పష్టమైన, సంక్షిప్తమైన నిర్వచనం లేదా వివరణను అందించండి (1-3 వాక్యాలు)\n"
                "2. ఉదాహరణలు: 2 సంబంధిత, ఉదాహరణాత్మక ఉదాహరణలను ఇవ్వండి\n"
                "3. అప్లికేషన్: సంక్షిప్తమైన ఆచరణాత్మక అప్లికేషన్ లేదా చిట్కాను అందించండి (1-2 వాక్యాలు)\n\n"
                "మీ సమాధానాన్ని కేంద్రీకృతం చేయండి, విద్యాపరమైనది మరియు సహాయకరమైనది."
            )
        }
    
    def _format_context(self, context: List[str], language_code: str) -> str:
        if not context:
            return ""
        
        context_header = {
            'en': "Previous conversation context:",
            'hi': "पिछले वार्तालाप का संदर्भ:",
            'te': "మునుపటి సంభాషణ సందర్భం:"
        }
        
        context_lines = [context_header[language_code]]
        for i, msg in enumerate(context[-3:], 1):
            context_lines.append(f"{i}. {msg}")
        
        return "\n".join(context_lines)
    
    def _get_final_instruction(self, language_code: str) -> str:
        final_instructions = {
            'en': (
                "Remember: Respond in the same language as the user's question. "
                "Be helpful, accurate, and educational. If you're unsure about "
                "something, say so rather than guessing."
            ),
            'hi': (
                "याद रखें: उपयोगकर्ता के प्रश्न की भाषा में ही जवाब दें। "
                "सहायक, सटीक और शैक्षिक बनें। यदि आप किसी चीज़ के बारे में "
                "अनिश्चित हैं, तो अनुमान लगाने के बजाय यह कहें।"
            ),
            'te': (
                "గుర్తుంచుకోండి: వినియోగదారు ప్రశ్న భాషలోనే సమాధానం ఇవ్వండి. "
                "సహాయకరంగా, ఖచ్చితంగా మరియు విద్యాపరంగా ఉండండి. మీరు ఏదైనా "
                "గురించి అనిశ్చితంగా ఉంటే, ఊహించే బదులు అలా చెప్పండి."
            )
        }
        
        return final_instructions[language_code]
    
    def build_error_prompt(self, language_code: str, error_type: str) -> str:
        error_templates = {
            'unsupported_language': {
                'en': (
                    "The user's message is in a language I don't support. "
                    "Please explain in English that I support English, Hindi, and Telugu, "
                    "and ask them to try again in one of these languages."
                ),
                'hi': (
                    "उपयोगकर्ता का संदेश एक ऐसी भाषा में है जिसे मैं समर्थन नहीं करता। "
                    "कृपया अंग्रेजी में समझाएं कि मैं अंग्रेजी, हिंदी और तेलुगु का समर्थन करता हूं, "
                    "और उन्हें इनमें से किसी एक भाषा में फिर से कोशिश करने के लिए कहें।"
                ),
                'te': (
                    "వినియోగదారు సందేశం నేను మద్దతు ఇవ్వని భాషలో ఉంది. "
                    "దయచేసి నేను ఆంగ్లం, హిందీ మరియు తెలుగును మద్దతు ఇస్తానని "
                    "ఆంగ్లంలో వివరించండి, మరియు వారిని ఈ భాషలలో ఒకటిలో "
                    "మళ్లీ ప్రయత్నించమని అడగండి."
                )
            },
            'api_error': {
                'en': (
                    "There was an error processing your request. "
                    "Please try again in a moment. If the problem persists, "
                    "check your internet connection and try again."
                ),
                'hi': (
                    "आपके अनुरोध को संसाधित करने में एक त्रुटि हुई। "
                    "कृपया कुछ देर बाद फिर से कोशिश करें। यदि समस्या बनी रहती है, "
                    "तो अपना इंटरनेट कनेक्शन जांचें और फिर से कोशिश करें।"
                ),
                'te': (
                    "మీ అభ్యర్థనను ప్రాసెస్ చేయడంలో ఒక లోపం ఉంది. "
                    "దయచేసి కొంత సమయం తర్వాత మళ్లీ ప్రయత్నించండి. "
                    "సమస్య కొనసాగితే, మీ ఇంటర్నెట్ కనెక్షన్‌ని తనిఖీ చేసి "
                    "మళ్లీ ప్రయత్నించండి."
                )
            }
        }
        
        template = error_templates.get(error_type, error_templates['api_error'])
        return template.get(language_code, template['en'])
    
    def get_language_specific_greeting(self, language_code: str) -> str:
        greetings = {
            'en': (
                "Hello! I'm your multilingual teacher assistant. "
                "I can help you with questions in English, Hindi, and Telugu. "
                "What would you like to learn about today?"
            ),
            'hi': (
                "नमस्ते! मैं आपका बहुभाषी शिक्षक सहायक हूं। "
                "मैं आपकी अंग्रेजी, हिंदी और तेलुगु में प्रश्नों के साथ मदद कर सकता हूं। "
                "आज आप क्या सीखना चाहते हैं?"
            ),
            'te': (
                "నమస్కారం! నేను మీ బహుభాషా ఉపాధ్యాయ సహాయకుడిని. "
                "నేను ఆంగ్లం, హిందీ మరియు తెలుగులో మీ ప్రశ్నలతో సహాయపడగలను. "
                "నేడు మీరు దేని గురించి నేర్చుకోవాలనుకుంటున్నారు?"
            )
        }
        
        return greetings.get(language_code, greetings['en'])
