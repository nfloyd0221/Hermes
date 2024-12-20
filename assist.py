import openai

# OpenAI API Configuration
openai.api_key = "your_openai_api_key"

def start_new_thread():
    """Start a new conversation thread."""
    response = openai.Assistant.create_thread()
    thread_id = response["id"]
    print(f"New thread started with ID: {thread_id}")
    return thread_id

def send_to_assistant(audio_file, thread_id):
    """Send user input to OpenAI Assistants API with thread handling."""
    with open(audio_file, "rb") as audio:
        # Transcribe audio to text using OpenAI Whisper
        transcription = openai.Audio.transcribe("whisper-1", audio)

    user_input = transcription["text"]
    print(f"User: {user_input}")

    # Send the transcribed text to the Assistant API
    response = openai.Assistant.create_message(
        thread_id=thread_id,
        input=user_input
    )

    assistant_response = response["output"]
    print(f"Assistant: {assistant_response}")
    return assistant_response
