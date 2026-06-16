"""
Command processor module.

Parses normalized voice commands and dispatches them to the appropriate
system, browser, integration, or termination handlers.
"""

import sys
import time

import pygame

from browser.browser_controller import (
    close_tab,
    new_tab,
    next_tab,
    previous_tab,
    switch_app,
)
from core.voice_engine import speak
from integrations.news_service import fetch_top_headlines
from integrations.youtube_service import play_on_youtube
from system.app_launcher import close_app, open_item
from system.system_controls import (
    log_out,
    mute_volume,
    report_battery,
    restart_system,
    shutdown_system,
    take_screenshot,
    tell_date,
    tell_time,
    volume_down,
    volume_up,
)
from system.window_manager import maximize_window, minimize_window
from utils.helpers import logger

# Module-level flag mirroring the original script's `stop_flag` and
# `listening` globals, used by terminate() and the command processor.
stop_flag = False
listening = True


def terminate() -> None:
    """
    Terminate Nexus.

    Speaks a goodbye message, stops the background listener loop, shuts
    down the pygame mixer, and exits the process.
    """
    global listening
    try:
        speak("Going to sleep. Goodbye!")
        listening = False
        pygame.mixer.quit()
    except Exception as e:
        logger.error("Error while terminating: %s", e)
        print(f"Error while terminating: {e}")
    sys.exit(0)


def processCommand(c: str) -> None:
    """
    Process a single voice command string and dispatch the matching action.

    Args:
        c: The raw recognized speech text to process.
    """
    global stop_flag
    c = c.lower().strip()
    print(f"Command: {c}")

    # --- NORMALIZE COMMANDS ---
    c = c.replace("launch", "open").replace("start", "open").replace("run", "open")
    c = c.replace("exit", "close").replace("quit", "close").replace("stop", "close")
    c = c.replace("the", "").strip()

    # --- MULTI OPEN COMMANDS ---
    if "open" in c and "and" in c:
        parts = c.split("and")
        for part in parts:
            if "open" in part:
                app_name = part.replace("open", "").strip()
                open_item(app_name)
                time.sleep(1)  # Small delay between openings
        return

    # --- MULTI CLOSE COMMANDS ---
    if "close" in c and "and" in c:
        parts = c.split("and")
        for part in parts:
            if "close" in part:
                app_name = part.replace("close", "").strip()
                close_app(app_name)
                time.sleep(1)
        return

    # --- OPEN SINGLE ITEM ---
    if "open" in c:
        app_name = c.replace("open", "").strip()
        open_item(app_name)
        return

    # --- CLOSE SINGLE ITEM ---
    if "close" in c:
        app_name = c.replace("close", "").strip()
        close_app(app_name)
        return

    # --- SYSTEM COMMANDS ---
    if "shutdown" in c:
        shutdown_system()
        return

    if "restart" in c:
        restart_system()
        return

    if "log out" in c:
        log_out()
        return

    # --- MISCELLANEOUS ---
    if "time" in c:
        tell_time()
        return

    if "date" in c:
        tell_date()
        return

    if "screenshot" in c:
        take_screenshot()
        return

    if "volume up" in c:
        volume_up()
        return

    if "volume down" in c:
        volume_down()
        return

    if "mute" in c:
        mute_volume()
        return

    if "battery" in c:
        report_battery()
        return

    if c.startswith("play "):
        song = c.replace("play ", "")
        play_on_youtube(song)
        return

        # --- WINDOW MANAGEMENT COMMANDS ---
    if "minimize" or "minimise" in c:
        if "window" in c:
            minimize_window()
        else:
            app_name = c.replace("minimize", "").strip()
            minimize_window(app_name)
        return

    if "maximize" in c:
        if "window" in c:
            maximize_window()
        else:
            app_name = c.replace("maximize", "").strip()
            maximize_window(app_name)
        return

    if "close tab" in c:
        close_tab()
        return

    if "new tab" in c:
        new_tab()
        return

    if "next tab" in c:
        next_tab()
        return

    if "previous tab" in c or "back tab" in c:
        previous_tab()
        return

    if "switch app" in c or "change window" in c:
        switch_app()
        return

    if "news" in c:
        fetch_top_headlines()
        return

    # --- TERMINATE ---
    if "sleep" in c or "goodbye" in c:
        terminate()
        return

    # --- FALLBACK ---
    speak("I didn't understand that. Please try again.")
