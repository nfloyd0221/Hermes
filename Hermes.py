#!/usr/bin/env python3

import os
import wave
import pyaudio
import speech_recognition as sr
import assist
import graphic


WAKE_WORD = "jarvis"  

def play_audio(filename):
    """Play an audio file"""
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

def wake_word_detection():
    """Listen for the wake word"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for wake word...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            transcript = recognizer.recognize_google(audio).lower()
            return WAKE_WORD in transcript
        except sr.UnknownValueError:
            print("Could not understand audio.")
    return False

def handle_command():
    """Handle a command after the wake word is detected."""
    graphic.start_graphic()  # Start dynamic graphics
    audio_file = record_audio()  # Record user command
    graphic.stop_graphic()  # Stop graphics after recording

    response = assist.send_to_assistant(audio_file)  # Send to Assistant API
    print(response)
    speech = response.split('#')[0]
    done = assist.TTS(speech)  # Convert text to speech and play it

def main():
    while True:
        if wake_word_detection():  # Detect the wake word
            print(f"Wake word '{WAKE_WORD}' detected!")
            
            # Handle the command then return to listening after each response
            handle_command()


if __name__ == "__main__":
    main()
