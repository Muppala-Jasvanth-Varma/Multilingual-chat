# 🚀 Deployment Guide for Streamlit Cloud

## Prerequisites
1. A GitHub account
2. A Streamlit Cloud account
3. A Google Gemini API key

## Step 1: Get Your Gemini API Key
1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Click "Get API key" or go to [API Keys](https://aistudio.google.com/app/apikey)
4. Create a new API key
5. Copy the API key (you'll need this for the next step)

## Step 2: Deploy to Streamlit Cloud
1. Go to [Streamlit Cloud](https://share.streamlit.io/)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository: `YOUR_USERNAME/Multilingual_Chat`
5. Set the main file path: `streamlit_app.py`
6. Click "Deploy!"

## Step 3: Configure API Key (IMPORTANT!)
1. In your deployed app, go to **Settings** (⚙️ icon)
2. Click **Secrets**
3. Add your API key in this format:
   ```toml
   GEMINI_API_KEY = "your_actual_api_key_here"
   ```
4. Click **Save**
5. Your app will automatically restart with the new configuration

## Step 4: Test Your App
1. Go back to your app
2. You should see "✅ Connected" in the sidebar
3. Try asking a question in any supported language!

## Troubleshooting

### ❌ "GEMINI_API_KEY not found" Error
- Make sure you added the API key to Streamlit secrets
- Check that the key name is exactly `GEMINI_API_KEY`
- Verify your API key is valid at [Google AI Studio](https://aistudio.google.com/)

### ❌ "Failed to initialize chatbot" Error
- Check your internet connection
- Verify your Gemini API key has sufficient quota
- Check the Streamlit Cloud logs for detailed error messages

### 🔄 App Not Updating
- Streamlit Cloud automatically restarts when you push to GitHub
- Check that your changes are committed and pushed
- Wait 1-2 minutes for deployment to complete

## Security Notes
- ✅ Your `.env` file is NOT uploaded to GitHub (protected by `.gitignore`)
- ✅ API keys in Streamlit secrets are encrypted and secure
- ✅ Never commit API keys to your repository

## Local Development
For local testing, create a `.env` file in your project root:
```bash
GEMINI_API_KEY=your_api_key_here
```

## Support
If you encounter issues:
1. Check the [Streamlit documentation](https://docs.streamlit.io/)
2. Check the [Gemini API documentation](https://ai.google.dev/docs)
3. Review the app logs in Streamlit Cloud
