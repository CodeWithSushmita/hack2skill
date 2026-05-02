import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

# We need to ensure we handle the case where the API key is not set.
# The new google-genai library will automatically pick up GEMINI_API_KEY from environment variables
# if we just instantiate the client.

def get_gemini_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None
    try:
        return genai.Client()
    except Exception as e:
        print(f"Error initializing Gemini Client: {e}")
        return None

def generate_text(prompt: str, model_name: str = "gemini-1.5-flash") -> str:
    """
    Utility function to generate text using the Gemini API.
    """
    client = get_gemini_client()
    if not client:
        return "Error: Gemini API key not configured or client initialization failed."
    
    try:
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"Error during generation: {str(e)}"
