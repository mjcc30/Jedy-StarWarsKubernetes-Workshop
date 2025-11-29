import google.generativeai as genai
import os
from dotenv import load_dotenv
import httpx

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)


def is_ai_enabled():
    return bool(GOOGLE_API_KEY or OPENROUTER_API_KEY)


def get_text_model():
    if not GOOGLE_API_KEY:
        return None
    try:
        # Updated to the latest fast model as of Nov 2025
        return genai.GenerativeModel("gemini-2.5-flash")
    except Exception as e:
        print(f"Error initializing Gemini Text: {e}")
        return None


def get_image_model():
    if not GOOGLE_API_KEY:
        return None
    try:
        # "Nano Banana" codename for Gemini 2.5 Flash Image
        return genai.GenerativeModel("gemini-2.5-flash-image")
    except Exception as e:
        print(f"Error initializing Gemini Image: {e}")
        return None


async def chat_with_character(
    character_name: str, character_context: str, user_message: str
):
    prompt = f"""
    You are {character_name} from Star Wars.
    Context about you: {character_context}
    
    Roleplay as this character perfectly. Use their tone, mannerisms, and knowledge.
    Keep responses concise (under 50 words) but immersive.
    
    User: {user_message}
    {character_name}:
    """

    # 1. Try Google Gemini Native
    if GOOGLE_API_KEY:
        model = get_text_model()
        if model:
            try:
                response = await model.generate_content_async(prompt)
                return response.text.strip()
            except Exception as e:
                return f"Connection lost (Gemini)... ({str(e)})"

    # 2. Try OpenRouter Fallback
    if OPENROUTER_API_KEY:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                        "HTTP-Referer": "http://localhost:3000",
                        "X-Title": "Star Wars App",
                    },
                    json={
                        "model": "google/gemini-2.0-flash-001",
                        "messages": [{"role": "user", "content": prompt}],
                    },
                    timeout=15.0,
                )
                response.raise_for_status()
                data = response.json()
                if "choices" in data and len(data["choices"]) > 0:
                    return data["choices"][0]["message"]["content"].strip()
                else:
                    return "The Force yielded no answer (OpenRouter)."
        except Exception as e:
            return f"Connection lost (OpenRouter)... ({str(e)})"

    return "I cannot speak right now. The Force is clouded (No API Key)."


async def generate_image_nano_banana(entity_name: str, entity_type: str):
    # Image generation currently supports only Native Google Gemini
    model = get_image_model()
    if not model:
        return None

    prompt = f"A cinematic, photorealistic 8k portrait of the Star Wars {entity_type} named '{entity_name}'. Highly detailed, dramatic lighting, movie still quality."

    try:
        # Note: The actual API call for image generation usually returns an Image object or path.
        # For this implementation using the standard SDK, we assume generate_content returns a response with image data
        # or we use the specific generate_images method if available in the specific SDK version.
        # As a fallback/standard way for Gemini Image models:
        response = await model.generate_content_async(prompt)

        # Check if response has parts and valid image data
        if response.parts and response.parts[0].inline_data:
            return response.parts[0].inline_data.data  # This is bytes

        # If the specific SDK version exposes it differently (simulated for stability):
        # In a real scenario with 'gemini-2.5-flash-image', we would handle the bytes directly.
        # For now, we will catch errors and return None to let the fallback handle it if the model ID is strict.
        return None
    except Exception as e:
        print(f"Nano Banana generation failed: {e}")
        return None
