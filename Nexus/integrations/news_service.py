"""
News service integration.

Fetches top headlines from NewsAPI and speaks them aloud.
"""

import requests

from config.settings import NEWS_API_KEY
from core.voice_engine import speak
from utils.helpers import logger


def fetch_top_headlines(country: str = "pk", limit: int = 5) -> None:
    """
    Fetch and speak the top news headlines for a given country.

    Args:
        country: Two-letter country code for NewsAPI (default: 'pk').
        limit: Maximum number of headlines to speak (default: 5).
    """
    try:
        speak("Fetching top headlines.")
        url = f"https://newsapi.org/v2/top-headlines?country={country}&apiKey={NEWS_API_KEY}"
        r = requests.get(url)
        data = r.json().get("articles", [])[:limit]
        for article in data:
            speak(article["title"])
    except Exception as e:
        logger.error("News error: %s", e)
        print("News error:", e)
        speak("Could not fetch news.")
