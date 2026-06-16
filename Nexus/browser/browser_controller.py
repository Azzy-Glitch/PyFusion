"""
Browser controller module.

Provides Chrome detection and tab-management actions (new tab, close tab,
next/previous tab) via keyboard shortcuts.
"""

import psutil
import pyautogui

from core.voice_engine import speak
from utils.helpers import logger


def is_chrome_running() -> bool:
    """
    Check whether the Chrome browser process is currently running.

    Returns:
        True if a process with 'chrome' in its name is found, False
        otherwise.
    """
    for proc in psutil.process_iter(["name"]):
        if "chrome" in proc.info["name"].lower():
            return True
    return False

def switch_app() -> None:
    """Switch to the most recently used application (Alt+Tab)."""
    try:
        pyautogui.hotkey("alt", "tab")
        speak("Switched to the previous application.")
    except Exception as e:
        logger.error("Error switching app: %s", e)
        print("Error switching app:", e)
        speak("I couldn't switch applications.")


def close_tab() -> None:
    """Close the current browser tab (Ctrl+W) if Chrome is running."""
    try:
        if is_chrome_running():
            pyautogui.hotkey("ctrl", "w")
            speak("Closed the tab.")
        else:
            speak("Chrome is not open, sir.")
    except Exception as e:
        logger.error("Error closing tab: %s", e)
        print("Error closing tab:", e)
        speak("I couldn't close the tab.")


def new_tab() -> None:
    """Open a new browser tab (Ctrl+T) if Chrome is running."""
    try:
        if is_chrome_running():
            pyautogui.hotkey("ctrl", "t")
            speak("Opened a new tab.")
        else:
            speak("Chrome is not open, sir.")
    except Exception as e:
        logger.error("Error opening new tab: %s", e)
        print("Error opening new tab:", e)
        speak("I couldn't open a new tab.")


def next_tab() -> None:
    """Switch to the next browser tab (Ctrl+Tab) if Chrome is running."""
    try:
        if is_chrome_running():
            pyautogui.hotkey("ctrl", "tab")
            speak("Switched to the next tab.")
        else:
            speak("Chrome is not open, sir.")
    except Exception as e:
        logger.error("Error switching tab: %s", e)
        print("Error switching tab:", e)
        speak("I couldn't switch to the next tab.")


def previous_tab() -> None:
    """Switch to the previous browser tab (Ctrl+Shift+Tab) if Chrome is running."""
    try:
        if is_chrome_running():
            pyautogui.hotkey("ctrl", "shift", "tab")
            speak("Switched to the previous tab.")
        else:
            speak("Chrome is not open, sir.")
    except Exception as e:
        logger.error("Error switching to previous tab: %s", e)
        print("Error switching to previous tab:", e)
        speak("I couldn't switch to the previous tab.")
