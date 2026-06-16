"""
Listener module.

Handles wake-word detection, background audio listening, and dispatching
recognized commands to the command processor on a separate thread.
"""

import threading
import time

import speech_recognition as sr

from config.settings import (
    AMBIENT_NOISE_DURATION,
    LISTENER_PHRASE_TIME_LIMIT,
    WAKE_WORD,
    WAKE_WORD_COOLDOWN,
)
from core.command_processor import processCommand, terminate
from core.voice_engine import speak
from utils.helpers import logger, play_beep

# === Initialization ===
recognizer = sr.Recognizer()

# === State ===
awake = False
command_thread = None


def callback(recognizer: sr.Recognizer, audio: sr.AudioData) -> None:
    """
    Process a chunk of audio captured by the background listener.

    If Nexus is not yet awake, checks for the wake word and, if found,
    acknowledges and plays a beep. If Nexus is already awake, treats the
    recognized text as a command and dispatches it to processCommand() on
    a new thread.

    Args:
        recognizer: The SpeechRecognition Recognizer instance.
        audio: The captured audio data to recognize.
    """
    global awake, command_thread
    import core.command_processor as command_processor

    try:
        text = recognizer.recognize_google(audio).lower().strip()
        print(f"Heard: {text}")

        if not awake:
            # Detect wake word
            if WAKE_WORD in text:
                awake = True
                speak("Yes sir?")
                play_beep()
            time.sleep(WAKE_WORD_COOLDOWN)

        else:
            # Already awake — process command
            awake = False
            command_processor.stop_flag = False
            command_thread = threading.Thread(target=processCommand, args=(text,))
            command_thread.start()

    except sr.UnknownValueError:
        pass
    except sr.RequestError:
        logger.warning("Speech recognition service error.")
        print("Speech recognition service error.")
    except Exception as e:
        logger.error("Callback error: %s", e)
        print("Callback error:", e)


def start_background_listener() -> None:
    """
    Initialize Nexus and start the background audio listener loop.

    Calibrates for ambient noise, begins listening in the background for
    the wake word and subsequent commands, and blocks until the
    `listening` flag in command_processor is set to False (e.g. via a
    'sleep' or 'goodbye' command), or until interrupted with Ctrl+C.
    """
    import core.command_processor as command_processor

    speak("Initializing Nexus... System ready!")
    mic = sr.Microphone()

    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=AMBIENT_NOISE_DURATION)
        print("Listening in background... Say 'Nexus' to wake me.")

    stop_listening = recognizer.listen_in_background(
        mic, callback, phrase_time_limit=LISTENER_PHRASE_TIME_LIMIT
    )

    try:
        while command_processor.listening:
            time.sleep(0.1)
    except KeyboardInterrupt:
        stop_listening(wait_for_stop=False)
        terminate()
