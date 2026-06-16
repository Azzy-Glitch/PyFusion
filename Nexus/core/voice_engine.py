"""
Voice engine module.

Handles text-to-speech output using gTTS (online, via pygame for playback)
with a fallback to pyttsx3 (offline) when no internet connection is
available or when an error occurs during online synthesis.
"""

import os
import uuid

import pygame
import pyttsx3
from gtts import gTTS

from config.settings import TTS_RATE, TTS_VOICE_NAME, TTS_VOLUME
from utils.helpers import is_online, logger

# === Initialization ===
pygame.mixer.init()

# Initialize pyttsx3 for offline TTS
tts_engine = pyttsx3.init()
voices = tts_engine.getProperty("voices")
for voice in voices:
    if TTS_VOICE_NAME in voice.name:
        tts_engine.setProperty("voice", voice.id)
        break
tts_engine.setProperty("rate", TTS_RATE)
tts_engine.setProperty("volume", TTS_VOLUME)


def speak(text: str) -> None:
    """
    Speak the given text aloud.

    Uses gTTS (online) for natural-sounding speech when an internet
    connection is available, playing the resulting audio via pygame.
    Falls back to pyttsx3 (offline) if there is no connection or if an
    error occurs during online synthesis/playback.

    Args:
        text: The text to be spoken.
    """
    print(f"Nexus: {text}")
    try:
        if is_online():
            filename = f"temp_{uuid.uuid4().hex}.mp3"
            tts = gTTS(text)
            tts.save(filename)
            pygame.mixer.init()
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            pygame.mixer.music.stop()
            pygame.mixer.quit()
            os.remove(filename)
        else:
            tts_engine.say(text)
            tts_engine.runAndWait()
    except Exception as e:
        logger.error("TTS error: %s", e)
        print("TTS error:", e)
        tts_engine.say(text)
        tts_engine.runAndWait()
