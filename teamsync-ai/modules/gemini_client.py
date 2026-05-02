import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Google Gemini
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

def call_llm(prompt: str, system_instruction: str = "You are a helpful AI assistant.") -> str:
    if not api_key:
        return "AI Error: GEMINI_API_KEY not found in environment."
        
    try:
        model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=system_instruction)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI Error: {str(e)}"
