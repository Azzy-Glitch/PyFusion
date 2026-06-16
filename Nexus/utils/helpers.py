"""
General-purpose helper utilities: connectivity checks, audio beeps, and
the shared logging configuration used across the Nexus project.
"""

import logging
import socket

import winsound

# === Logger Setup ===
logger = logging.getLogger("nexus")
if not logger.handlers:
    _handler = logging.StreamHandler()
    _formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )
    _handler.setFormatter(_formatter)
    logger.addHandler(_handler)
    logger.setLevel(logging.INFO)


def is_online(host: str = "www.google.com", port: int = 80, timeout: float = 2.0) -> bool:
    """
    Check whether an internet connection is available.

    Args:
        host: Host to attempt a connection to.
        port: Port to connect on.
        timeout: Connection timeout in seconds.

    Returns:
        True if a connection could be established, False otherwise.
    """
    try:
        socket.create_connection((host, port), timeout=timeout)
        return True
    except OSError:
        return False


def play_beep() -> None:
    """Play a short notification beep (Windows only, via winsound)."""
    winsound.Beep(1000, 500)
