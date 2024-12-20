import openai
import os

# OpenAI API Configuration
openai.api_key = "your_openai_api_key"

def generate_tts(text):
    """Convert text to speech using OpenAI TTS API."""
    response = openai.Audio.generate(
        model="voice-1",
        input=text
    )

    audio_file = "response.wav"
    with open(audio_file, "wb") as f:
        f.write(response["audio"])
    return audio_file
