import os
import time
import re
from pygame import mixer
import speech_recognition as sr
import openai
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key_temp = os.getenv("OPENAI_API_KEY")

# OpenAI API Configuration
client = OpenAI(default_headers={"OpenAI-Beta": "assistants=v2"}, api_key=api_key_temp)
mixer.init()

assistant_id = "asst_e1lRtkunXL6VOgsuiLRERBhK"
thread_id = "thread_DQ6XrRj0Nx9gIvrmZVd1gMRS"

assistant = client.beta.assistants.retrieve(assistant_id)
thread = client.beta.threads.retrieve(thread_id)

def transcribe_audio_google(audio_file):
    """Transcribe audio"""
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)  # Read the entire audio file
    try:
        # Use google SST
        transcript = recognizer.recognize_google(audio)
        print(f"User: {transcript}")
        return transcript
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio.")
        return ""
    except sr.RequestError:
        print("Could not request results from Google Speech Recognition service.")
        return ""

def send_to_assistant(audio_file):
    """Send user input to OpenAI Assistants API in existing thread."""
    transcription = transcribe_audio_google(audio_file)

    if not transcription:
        return "Failed to transcribe audio."

    # Send the transcribed text to the Assistant API
    global thread
    response = client.beta.threads.messages.create(
        thread.id,
        role="user",
        content=transcription
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id
    )
    
    while (run_status := client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id)).status != 'completed':
        if run_status.status == 'failed':
            return "The run failed."
        time.sleep(1)
    
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    return messages.data[0].content[0].text.value

def generate_tts(sentence, speech_file_path):
    response = client.audio.speech.create(model="tts-1", voice="echo", input=sentence)
    response.stream_to_file(speech_file_path)
    return str(speech_file_path)

def play_sound(file_path):
    mixer.music.load(file_path)
    mixer.music.play()

def TTS(text):
    # Remove any [number] patterns from the text
    cleaned_text = re.sub(r'\[\d+\]', '', text).strip()
    
    # Ensure the text isn't empty before proceeding with TTS
    if not cleaned_text:
        cleaned_text = "Sorry, I couldn't understand that."

    speech_file_path = generate_tts(cleaned_text, "speech.mp3")
    play_sound(speech_file_path)
    while mixer.music.get_busy():
        time.sleep(1)
    mixer.music.unload()
    os.remove(speech_file_path)
    return "done"