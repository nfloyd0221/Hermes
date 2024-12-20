import os
import wave
import pyaudio
import speech_recognition as sr
import assistant_api
import tts_api

# Configurations
WAKE_WORD = "Jarvis"  # Change as needed

def play_audio(filename):
    """Play an audio file using PyAudio."""
    chunk = 1024
    wf = wave.open(filename, 'rb')
    pa = pyaudio.PyAudio()

    stream = pa.open(
        format=pa.get_format_from_width(wf.getsampwidth()),
        channels=wf.getnchannels(),
        rate=wf.getframerate(),
        output=True
    )

    data = wf.readframes(chunk)
    while data:
        stream.write(data)
        data = wf.readframes(chunk)

    stream.stop_stream()
    stream.close()
    pa.terminate()

def dynamic_graphic():
    """Placeholder for dynamic graphic while listening."""
    print("Listening... (dynamic graphic here)")  # Replace with your code

def record_audio():
    """Record audio from the user."""
    chunk = 1024
    sample_format = pyaudio.paInt16
    channels = 1
    rate = 44100
    record_seconds = 5
    filename = "command.wav"

    p = pyaudio.PyAudio()
    stream = p.open(format=sample_format, channels=channels,
                    rate=rate, input=True, frames_per_buffer=chunk)

    print("Recording...")
    frames = []

    for _ in range(0, int(rate / chunk * record_seconds)):
        data = stream.read(chunk)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()

    return filename

def wake_word_detected():
    """Listen for the wake word using a microphone."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for wake word...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            transcript = recognizer.recognize_google(audio).lower()
            return WAKE_WORD in transcript
        except sr.UnknownValueError:
            print("Could not understand audio.")
        except sr.WaitTimeoutError:
            print("Listening timed out.")
    return False

def main():
    while True:
        if wake_word_detected():
            print(f"Wake word '{WAKE_WORD}' detected!")
            thread_id = assistant_api.start_new_thread()  # Start a new thread
            while True:
                dynamic_graphic()  # Show dynamic graphic
                audio_file = record_audio()  # Record user command
                user_text = assistant_api.send_to_assistant(audio_file, thread_id)  # Send to Assistant API
                
                if "thank you" in user_text.lower():
                    print("User said 'thank you'. Ending session.")
                    break

                audio_response = tts_api.generate_tts(user_text)  # Generate TTS response
                play_audio(audio_response)  # Play TTS response

if __name__ == "__main__":
    main()
