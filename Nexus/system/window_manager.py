"""
Window management module.

Provides functions to minimize/maximize windows (either a named window or
the active one) and to switch between open applications.
"""

from typing import Optional

import pyautogui
import pygetwindow as gw

from core.voice_engine import speak
from utils.helpers import logger


def minimize_window(app_name: Optional[str] = None) -> None:
    """
    Minimize a window or the currently active one if no app is specified.

    Args:
        app_name: Optional title (or partial title) of the window to
            minimize. If None, minimizes the active window via the
            Win+Down shortcut.
    """
    try:
        if app_name:
            windows = [w for w in gw.getWindowsWithTitle(app_name) if w.isVisible]
            if windows:
                windows[0].minimize()
                speak(f"Minimized {app_name}")
                return
        pyautogui.hotkey("win", "down")
        speak("Window minimized")
    except Exception as e:
        logger.error("Error minimizing window: %s", e)
        print("Error minimizing window:", e)
        speak("I couldn't minimize that window.")


def maximize_window(app_name: Optional[str] = None) -> None:
    """
    Maximize a window or the currently active one if no app is specified.

    Args:
        app_name: Optional title (or partial title) of the window to
            maximize. If None, maximizes the active window via the
            Win+Up shortcut.
    """
    try:
        if app_name:
            windows = [w for w in gw.getWindowsWithTitle(app_name) if w.isVisible]
            if windows:
                win = windows[0]
                if not win.isMaximized:
                    win.maximize()
                speak(f"Maximized {app_name}")
                return
        pyautogui.hotkey("win", "up")
        speak("Window maximized")
    except Exception as e:
        logger.error("Error maximizing window: %s", e)
        print("Error maximizing window:", e)
        speak("I couldn't maximize that window.")


def switch_app() -> None:
    """Switch to another application using the Alt+Tab shortcut."""
    try:
        pyautogui.hotkey("alt", "tab")
        speak("Switched app.")
    except Exception as e:
        logger.error("Error switching app: %s", e)
        print("Error switching app:", e)
        speak("I couldn't switch the app.")
