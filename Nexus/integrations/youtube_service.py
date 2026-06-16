"""
YouTube service integration.

Plays a requested song/video on YouTube using pywhatkit.
"""

import pywhatkit

from core.voice_engine import speak


def play_on_youtube(song: str) -> None:
    """
    Play a song/video on YouTube.

    Args:
        song: The name of the song or video to search for and play.
    """
    speak(f"Playing {song} on YouTube")
    pywhatkit.playonyt(song)
