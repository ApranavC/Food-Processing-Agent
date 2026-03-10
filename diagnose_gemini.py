import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

def list_models():
    api_key = "AIzaSyCnRfUb5BADO_iaUYbvLca5s1MCH7kO58A"
    if not api_key:
        print("GOOGLE_API_KEY NOT FOUND.")
        print("Usage: GOOGLE_API_KEY=your_key_here python diagnose_gemini.py")
        return

    client = genai.Client(api_key=api_key)
    print(f"Listing available models for your API key...")
    try:
        # Use the new SDK method to list models
        for m in client.models.list():
            print(f"- {m.name}")
    except Exception as e:
        print(f"Error diagnostics: {e}")

if __name__ == "__main__":
    list_models()
