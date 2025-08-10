# Multilingual Teacher Chatbot

A Python-based chatbot that provides teacher-style responses in English, Hindi, and Telugu. The bot automatically detects the input language and responds in the same language with structured educational content.

## Features

- **Multilingual Support**: English, Hindi, and Telugu
- **Automatic Language Detection**: Detects user input language automatically
- **Teacher-Style Responses**: Structured format with definitions, examples, and practical applications
- **Conversational Context**: Maintains session-based conversation history
- **Multiple Interfaces**: CLI and Streamlit web UI
- **Easy API Integration**: Modular design for easy LLM provider switching

## Architecture

```
Multilingual_Chat/
├── chatbot/           # Core chatbot modules
│   ├── __init__.py
│   ├── client.py      # LLM API wrapper (Gemini)
│   ├── language.py    # Language detection utilities
│   ├── prompt_builder.py # Teacher-style prompt construction
│   ├── session.py     # Session/context management
│   └── utils.py       # Helper functions
├── examples/          # Example interactions
├── main.py           # CLI interface
├── streamlit_app.py  # Streamlit web UI
├── requirements.txt  # Dependencies
└── .env.example     # Environment variables template
```

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your Gemini API key:

```bash
GEMINI_API_KEY=your_actual_api_key_here
```

**Getting a Gemini API Key:**
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key to your `.env` file

### 3. Run the Application

#### CLI Interface
```bash
python main.py
```

#### Streamlit Web UI
```bash
streamlit run streamlit_app.py
```

## Usage Examples

### English Input
```
User: What is photosynthesis?
Bot: Photosynthesis is the process by which plants convert sunlight, carbon dioxide, and water into glucose and oxygen.

Examples:
1. Green leaves use sunlight to make food from air and water
2. Algae in ponds produce oxygen through this process

Application: Understanding photosynthesis helps us appreciate how plants support life on Earth and why protecting forests is crucial.
```

### Hindi Input
```
User: प्रकाश संश्लेषण क्या है?
Bot: प्रकाश संश्लेषण वह प्रक्रिया है जिसके द्वारा पौधे सूर्य के प्रकाश, कार्बन डाइऑक्साइड और पानी को ग्लूकोज और ऑक्सीजन में बदलते हैं।

Examples:
1. हरे पत्ते सूर्य के प्रकाश का उपयोग करके हवा और पानी से भोजन बनाते हैं
2. तालाबों में शैवाल इस प्रक्रिया के माध्यम से ऑक्सीजन का उत्पादन करते हैं

Application: प्रकाश संश्लेषण को समझने से हमें यह समझने में मदद मिलती है कि पौधे पृथ्वी पर जीवन का समर्थन कैसे करते हैं और जंगलों की रक्षा करना क्यों महत्वपूर्ण है।
```

### Telugu Input
```
User: కిరణజన్య సంయోగ క్రియ అంటే ఏమిటి?
Bot: కిరణజన్య సంయోగ క్రియ అనేది మొక్కలు సూర్యరశ్మి, కార్బన్ డయాక్సైడ్ మరియు నీటిని గ్లూకోజ్ మరియు ఆక్సిజన్గా మార్చే ప్రక్రియ.

Examples:
1. ఆకుపచ్చ ఆకులు సూర్యరశ్మిని ఉపయోగించి గాలి మరియు నీటి నుండి ఆహారాన్ని తయారు చేస్తాయి
2. చెరువులలో ఉన్న శైవలాలు ఈ ప్రక్రియ ద్వారా ఆక్సిజన్ను ఉత్పత్తి చేస్తాయి

Application: కిరణజన్య సంయోగ క్రియను అర్థం చేసుకోవడం మొక్కలు భూమిపై జీవితానికి ఎలా మద్దతు ఇస్తాయి మరియు అడవులను రక్షించడం ఎందుకు క్లిష్టమైనది అని అర్థం చేసుకోవడానికి మాకు సహాయపడుతుంది.
```

## Testing

### Manual Testing
1. Run the CLI: `python main.py`
2. Test each language with sample inputs
3. Verify responses are in the same language
4. Check that responses follow teacher format

### Automated Testing
```bash
python -m pytest tests/
```

## Configuration Options

### Language Detection
- **Auto-detection**: Default behavior
- **Force language**: Use `--lang` flag in CLI
- **Fallback**: English for unsupported languages

### Response Format
- **Definition**: 1-3 sentences
- **Examples**: 2 relevant examples
- **Application**: 1-2 practical sentences

## Error Handling

- **Unsupported Language**: Polite English explanation
- **API Errors**: Retry with exponential backoff
- **Invalid Input**: Sanitized and safe processing
- **Network Issues**: Clear error messages

## Performance Considerations

- **API Costs**: ~$0.001-0.01 per response (Gemini pricing)
- **Response Time**: 1-3 seconds typical
- **Session Memory**: In-memory storage (configurable)

## Optional Improvements

- **Caching**: Redis/sqlite for response caching
- **Local Models**: fastText for language detection
- **Speech**: Text-to-speech and speech-to-text
- **Persistence**: Database session storage
- **Rate Limiting**: API call throttling

## Safety Notes

- **Hallucination Risk**: LLM responses may contain inaccuracies
- **Content Filtering**: Implement additional safety checks if needed
- **API Limits**: Respect rate limits and usage quotas

## Troubleshooting

### Common Issues

1. **API Key Error**: Check `.env` file and API key validity
2. **Language Detection Failures**: Use `--lang` flag to force language
3. **Slow Responses**: Check internet connection and API status
4. **Import Errors**: Ensure all dependencies are installed

### Support

For issues or questions:
1. Check the examples in the `examples/` directory
2. Verify your API key and environment setup
3. Test with simple inputs first

## License

MIT License - see LICENSE file for details.
