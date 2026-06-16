"""
System control module.

Handles power operations (shutdown, restart, log out), time/date queries,
screenshots, volume control, and battery status reporting.
"""

import datetime
import os
import time

import psutil
import pyautogui

from core.voice_engine import speak


def shutdown_system() -> None:
    """Shut down the computer after a short delay."""
    speak("Shutting down your computer.")
    os.system("shutdown /s /t 5")


def restart_system() -> None:
    """Restart the computer after a short delay."""
    speak("Restarting your computer.")
    os.system("shutdown /r /t 5")


def log_out() -> None:
    """Sign the current user out of Windows."""
    speak("Signing out.")
    os.system("shutdown /l")


def tell_time() -> None:
    """Speak the current time in 12-hour format."""
    speak(f"The time is {datetime.datetime.now().strftime('%I:%M %p')}")


def tell_date() -> None:
    """Speak today's date."""
    speak(f"Today is {datetime.datetime.now().strftime('%A, %d %B %Y')}")


def take_screenshot() -> None:
    """Capture a screenshot and save it with a timestamped filename."""
    filename = f"screenshot_{time.strftime('%Y%m%d-%H%M%S')}.png"
    pyautogui.screenshot(filename)
    speak(f"Screenshot saved as {filename}")


def volume_up() -> None:
    """Increase the system volume by one step."""
    pyautogui.press("volumeup")
    speak("Volume increased.")


def volume_down() -> None:
    """Decrease the system volume by one step."""
    pyautogui.press("volumedown")
    speak("Volume decreased.")


def mute_volume() -> None:
    """Toggle system volume mute."""
    pyautogui.press("volumemute")
    speak("Volume muted.")


def report_battery() -> None:
    """Speak the current battery percentage and charging status."""
    battery = psutil.sensors_battery()
    speak(f"Battery is at {battery.percent} percent.")
    speak("Charging." if battery.power_plugged else "Not charging.")
