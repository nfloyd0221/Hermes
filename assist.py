import openai
from openai import OpenAI
import os
from pygame import mixer
import time

api_key_temp = os.environ['OPENAI_API_KEY']
print(api_key_temp)
# OpenAI API Configuration
client = OpenAI(default_headers={"OpenAI-Beta": "assistants=v2"}, api_key = api_key_temp)
mixer.init()

assistant_id = "asst_e1lRtkunXL6VOgsuiLRERBhK"
thread_id = "thread_PuIFMd18KmXJMNWSpPLvjS06"

assistant = client.beta.assistants.retrieve(assistant_id)
thread = client.beta.threads.retrieve(thread_id)


def send_to_assistant(audio_file):
    """Send user input to OpenAI Assistants API with thread handling."""
    with open(audio_file, 'rb') as audio:
        # Transcribe audio to text using OpenAI Whisper
        transcription = client.audio.transcriptions.create(model="whisper-1", file=audio)

    print(f"User: {transcription.text}")

    # Send the transcribed text to the Assistant API
    global thread
    response = client.beta.threads.messages.create(
        thread.id,
        role="user",
        content=transcription.text
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
    speech_file_path = generate_tts(text, "speech.mp3")
    play_sound(speech_file_path)
    while mixer.music.get_busy():
        time.sleep(1)
    mixer.music.unload()
    os.remove(speech_file_path)
    return "done"
