"""
Central application settings.

API keys and other environment-specific values are read from environment
variables so secrets are not hard-coded in source. A fallback default is
provided for the News API key to preserve the original script's behavior
if the environment variable is not set.
"""

import os

# News API key (set NEWS_API_KEY in your environment for production use).
# Falls back to the key embedded in the original script if not provided,
# to preserve original behavior out-of-the-box.
NEWS_API_KEY: str = os.environ.get("NEWS_API_KEY", "7ff93445a6ea436facbbf16144903512")

# Wake word used to activate Nexus.
WAKE_WORD: str = "nexus"

# Cooldown (in seconds) applied after wake-word detection.
WAKE_WORD_COOLDOWN: float = 0.3

# Preferred pyttsx3 voice name substring (offline TTS fallback).
TTS_VOICE_NAME: str = "Zira"

# pyttsx3 speech rate and volume.
TTS_RATE: int = 150
TTS_VOLUME: float = 0.9

# Phrase time limit (seconds) for background listener.
LISTENER_PHRASE_TIME_LIMIT: int = 6

# Ambient noise calibration duration (seconds).
AMBIENT_NOISE_DURATION: float = 1.0
