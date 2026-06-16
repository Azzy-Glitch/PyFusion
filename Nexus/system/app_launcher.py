"""
Application launcher module.

Resolves voice commands to launch or close system utilities, third-party
applications, or websites, based on the configuration dictionaries.
"""

import os
import subprocess

from config.apps import APPS
from config.sites import SITES
from config.system_apps import SYSTEM_APPS
from core.voice_engine import speak
from utils.helpers import logger


def open_item(name: str) -> None:
    """
    Open a system app, third-party application, or website by name.

    Performs exact-match lookups first against system apps, regular apps,
    and websites (in that order), then falls back to partial (substring)
    matches across the same dictionaries. Speaks a confirmation or
    failure message accordingly.

    Args:
        name: The name of the item to open, as spoken by the user.
    """
    name = name.lower().strip()
    print(f"Trying to open: {name}")

    # First check system apps
    if name in SYSTEM_APPS:
        speak(f"Opening {name}")
        try:
            subprocess.Popen(SYSTEM_APPS[name], shell=True)
            return
        except Exception as e:
            logger.error("Error opening system app: %s", e)
            print(f"Error opening system app: {e}")
            speak(f"Sorry, couldn't open {name}")

    # Check regular apps
    elif name in APPS:
        speak(f"Opening {name}")
        try:
            os.system(f'start "" "{APPS[name]}"')
            return
        except Exception as e:
            logger.error("Error opening app: %s", e)
            print(f"Error opening app: {e}")
            speak(f"Sorry, couldn't open {name}")

    # Check websites
    elif name in SITES:
        speak(f"Opening {name}")
        import webbrowser
        webbrowser.open(SITES[name])
        return

    # Partial matches
    else:
        # Check partial matches in system apps
        for sys_app, command in SYSTEM_APPS.items():
            if name in sys_app:
                speak(f"Opening {sys_app}")
                subprocess.Popen(command, shell=True)
                return

        # Check partial matches in regular apps
        for app_name, path in APPS.items():
            if name in app_name:
                speak(f"Opening {app_name}")
                os.system(f'start "" "{path}"')
                return

        # Check partial matches in websites
        for site_name, url in SITES.items():
            if name in site_name:
                speak(f"Opening {site_name}")
                import webbrowser
                webbrowser.open(url)
                return

    # If nothing found
    speak(f"Sorry, I couldn't find {name}.")


def close_app(app_name: str) -> None:
    """
    Close a running application by name.

    Performs an exact match against the regular apps dictionary first,
    then a partial (substring) match. If the name matches a system app,
    informs the user it cannot be closed this way. As a final fallback,
    attempts to kill a process named '<app_name>.exe'.

    Args:
        app_name: The name of the application to close, as spoken by the
            user.
    """
    app_name = app_name.lower().strip()
    print(f"Trying to close: {app_name}")

    # Find the process name from apps dictionary
    process_name = None

    # Exact match in apps
    if app_name in APPS:
        process_name = APPS[app_name]
        speak(f"Closing {app_name}")

    # Partial match in apps
    else:
        for app_key, app_exe in APPS.items():
            if app_name in app_key:
                process_name = app_exe
                speak(f"Closing {app_key}")
                break
        else:
            # If not found in apps, try system apps
            if app_name in SYSTEM_APPS:
                speak(f"{app_name} is a system app and cannot be closed this way")
                return
            else:
                # Final fallback - try app_name.exe
                process_name = app_name + ".exe"
                speak(f"Attempting to close {app_name}")

    try:
        # Close the app
        result = os.system(f"taskkill /IM {process_name} /F >nul 2>&1")
        if result == 0:
            speak(f"Successfully closed {app_name}")
        else:
            speak(f"{app_name} is not running or couldn't be closed")
    except Exception as e:
        logger.error("Error closing app: %s", e)
        print("Error closing app:", e)
        speak(f"Sorry, I couldn't close {app_name}")
