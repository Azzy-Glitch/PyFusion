"""
Nexus Voice Assistant - Entry point.

Run this module to start Nexus. It initializes the background listener,
which waits for the wake word ("nexus") and then processes spoken
commands until a 'sleep' or 'goodbye' command is received, or the process
is interrupted (Ctrl+C).
"""

from core.listener import start_background_listener


def main() -> None:
    """Start the Nexus background listener."""
    start_background_listener()


if __name__ == "__main__":
    main()
