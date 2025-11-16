# === Imports ===
import speech_recognition as sr
import webbrowser
import requests
from gtts import gTTS
import pygame
import os
import pywhatkit
import datetime
import psutil
import time
import pyautogui
import threading
import uuid
import sys
import pyttsx3
import socket
import subprocess
import winsound 
import pygetwindow as gw

# === Initialization ===
recognizer = sr.Recognizer()
pygame.mixer.init()
newsapi = "7ff93445a6ea436facbbf16144903512"

stop_flag = False
listening = True
command_thread = None

# Initialize pyttsx3 for offline TTS
tts_engine = pyttsx3.init()
voices = tts_engine.getProperty('voices')
for voice in voices:
    if "Zira" in voice.name:
        tts_engine.setProperty('voice', voice.id)
        break
tts_engine.setProperty('rate', 150)
tts_engine.setProperty('volume', 0.9)

# === Check Internet Connection ===
def is_online():
    try:
        socket.create_connection(("www.google.com", 80), timeout=2)
        return True
    except OSError:
        return False

# === Text-to-Speech ===
def speak(text):
    print(f"Nexus: {text}")
    try:
        if is_online():
            filename = f"temp_{uuid.uuid4().hex}.mp3"
            tts = gTTS(text)
            tts.save(filename)
            pygame.mixer.init()
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            pygame.mixer.music.stop()
            pygame.mixer.quit()
            os.remove(filename)
        else:
            tts_engine.say(text)
            tts_engine.runAndWait()
    except Exception as e:
        print("TTS error:", e)
        tts_engine.say(text)
        tts_engine.runAndWait()

# === Windows System Apps Dictionary ===
system_apps = {
    "control panel": "control",
    "task manager": "taskmgr",
    "file explorer": "explorer",
    "command prompt": "cmd",
    "powershell": "powershell",
    "calculator": "calc",
    "notepad": "notepad",
    "paint": "mspaint",
    "wordpad": "write",
    "character map": "charmap",
    "device manager": "devmgmt.msc",
    "disk management": "diskmgmt.msc",
    "services": "services.msc",
    "event viewer": "eventvwr",
    "system configuration": "msconfig",
    "registry editor": "regedit",
    "computer management": "compmgmt.msc",
    "windows features": "optionalfeatures",
    "programs and features": "appwiz.cpl",
    "network connections": "ncpa.cpl",
    "power options": "powercfg.cpl",
    "sound settings": "mmsys.cpl",
    "display settings": "desk.cpl",
    "mouse settings": "main.cpl",
    "keyboard settings": "control keyboard",
    "date and time": "timedate.cpl",
    "region settings": "intl.cpl",
    "user accounts": "netplwiz",
    "windows security": "windowsdefender:",
    "printer settings": "control printers",
    "bluetooth settings": "fsquirt",
    "windows update": "ms-settings:windowsupdate",
    "settings": "ms-settings:",
    "run dialog": "winver",
    "system information": "msinfo32",
    "resource monitor": "resmon",
    "performance monitor": "perfmon",
    "clipboard": "win+v",
    "magnifier": "magnify",
    "narrator": "narrator",
    "on-screen keyboard": "osk",
    "windows media player": "wmplayer",
    "sound recorder": "soundrecorder",
    "sticky notes": "stikynot",
    "snipping tool": "snippingtool",
    "xbox game bar": "gamebar",
    "camera": "microsoft.windows.camera:",
    "photos": "ms-photos:",
    "calendar": "outlookcal:",
    "mail": "outlookmail:",
    "store": "ms-windows-store:",
    "weather": "msnweather:",
    "news": "msnnews:",
    "sports": "msnsports:",
    "money": "msnmoney:",
    "travel": "msntravel:"
}

# === Regular Apps Dictionary ===
apps = {
    "chrome": "chrome.exe",
    "edge": "msedge.exe",
    "firefox": "firefox.exe",
    "opera": "opera.exe",
    "code": "code.exe",
    "visual studio": "devenv.exe",
    "pycharm": "pycharm64.exe",
    "intellij": "idea64.exe",
    "android studio": "studio64.exe",
    "eclipse": "eclipse.exe",
    "netbeans": "netbeans64.exe",
    "word": "winword.exe",
    "excel": "excel.exe",
    "powerpoint": "powerpnt.exe",
    "outlook": "outlook.exe",
    "onenote": "onenote.exe",
    "access": "msaccess.exe",
    "publisher": "mspub.exe",
    "visio": "visio.exe",
    "project": "winproj.exe",
    "teams": "teams.exe",
    "skype": "skype.exe",
    "zoom": "zoom.exe",
    "discord": "discord.exe",
    "slack": "slack.exe",
    "whatsapp": "whatsapp.exe",
    "telegram": "telegram.exe",
    "vscode": "code.exe",
    "notepad": "notepad++.exe",
    "sublime": "sublime_text.exe",
    "atom": "atom.exe",
    "photoshop": "photoshop.exe",
    "illustrator": "illustrator.exe",
    "premiere": "premiere.exe",
    "after effects": "afterfx.exe",
    "lightroom": "lightroom.exe",
    "acrobat": "acrobat.exe",
    "reader": "acrord32.exe",
    "winrar": "winrar.exe",
    "7zip": "7zfm.exe",
    "winzip": "winzip64.exe",
    "spotify": "spotify.exe",
    "vlc": "vlc.exe",
    "media player": "wmplayer.exe",
    "quicktime": "quicktimeplayer.exe",
    "itunes": "itunes.exe",
    "steam": "steam.exe",
    "epic games": "epicgameslauncher.exe",
    "origin": "origin.exe",
    "battle.net": "battle.net.exe",
    "utorrent": "utorrent.exe",
    "bittorrent": "bittorrent.exe",
    "qbittorrent": "qbittorrent.exe",
    "teamviewer": "teamviewer.exe",
    "anydesk": "anydesk.exe",
    "ccleaner": "ccleaner64.exe",
    "malwarebytes": "mbam.exe",
    "avast": "avastui.exe",
    "avg": "avgui.exe",
    "norton": "norton.exe",
    "kaspersky": "avp.exe",
    "python": "python.exe",
    "java": "javaw.exe",
    "node": "node.exe",
    "git": "git-bash.exe",
    "docker": "docker.exe",
    "postman": "postman.exe",
    "mysql": "mysql.exe",
    "workbench": "mysqlworkbench.exe",
    "mongodb": "mongodb.exe",
    "redis": "redis-server.exe",
    "virtualbox": "virtualbox.exe",
    "vmware": "vmware.exe",
    "hyper-v": "vmconnect.exe",
    "blender": "blender.exe",
    "maya": "maya.exe",
    "3ds max": "3dsmax.exe",
    "cinema 4d": "cinema4d.exe",
    "unity": "unity.exe",
    "unreal": "unrealengine.exe",
    "godot": "godot.exe",
    "obs": "obs64.exe",
    "streamlabs": "streamlabs.exe",
    "xsplit": "xsplit.exe",
    "camtasia": "camtasia.exe",
    "audacity": "audacity.exe",
    "gimp": "gimp-2.10.exe",
    "inkscape": "inkscape.exe",
    "krita": "krita.exe",
    "lightshot": "lightshot.exe",
    "sharex": "sharex.exe",
    "greenshot": "greenshot.exe",
    "onenote": "onenote.exe",
    "evernote": "evernote.exe",
    "notion": "notion.exe",
    "todoist": "todoist.exe",
    "trello": "trello.exe",
    "asana": "asana.exe",
    "clickup": "clickup.exe"
}

# === Websites Dictionary ===
sites = {
    "google": "https://www.google.com",
    "youtube": "https://www.youtube.com",
    "facebook": "https://www.facebook.com",
    "instagram": "https://www.instagram.com",
    "twitter": "https://www.twitter.com",
    "linkedin": "https://www.linkedin.com",
    "github": "https://www.github.com",
    "stackoverflow": "https://stackoverflow.com",
    "reddit": "https://www.reddit.com",
    "wikipedia": "https://www.wikipedia.org",
    "amazon": "https://www.amazon.com",
    "netflix": "https://www.netflix.com",
    "spotify": "https://www.spotify.com",
    "gmail": "https://mail.google.com",
    "outlook": "https://outlook.live.com",
    "drive": "https://drive.google.com",
    "dropbox": "https://www.dropbox.com",
    "whatsapp": "https://web.whatsapp.com",
    "telegram": "https://web.telegram.org",
    "discord": "https://discord.com",
    "twitch": "https://www.twitch.tv",
    "microsoft": "https://www.microsoft.com",
    "apple": "https://www.apple.com",
    "ubuntu": "https://ubuntu.com",
    "wordpress": "https://wordpress.com",
    "medium": "https://medium.com",
    "quora": "https://www.quora.com",
    "pinterest": "https://www.pinterest.com",
    "tumblr": "https://www.tumblr.com",
    "flickr": "https://www.flickr.com",
    "imgur": "https://imgur.com",
    "unsplash": "https://unsplash.com",
    "deviantart": "https://www.deviantart.com",
    "behance": "https://www.behance.net",
    "dribbble": "https://dribbble.com",
    "figma": "https://www.figma.com",
    "canva": "https://www.canva.com",
    "notion": "https://www.notion.so",
    "trello": "https://trello.com",
    "asana": "https://asana.com",
    "slack": "https://slack.com",
    "zoom": "https://zoom.us",
    "teams": "https://teams.microsoft.com",
    "skype": "https://web.skype.com",
    "signal": "https://signal.org",
    "paypal": "https://www.paypal.com",
    "stripe": "https://stripe.com",
    "coinbase": "https://www.coinbase.com",
    "binance": "https://www.binance.com",
    "kraken": "https://www.kraken.com",
    "booking": "https://www.booking.com",
    "airbnb": "https://www.airbnb.com",
    "tripadvisor": "https://www.tripadvisor.com",
    "expedia": "https://www.expedia.com",
    "kayak": "https://www.kayak.com",
    "uber": "https://www.uber.com",
    "lyft": "https://www.lyft.com",
    "doordash": "https://www.doordash.com",
    "ubereats": "https://www.ubereats.com",
    "grubhub": "https://www.grubhub.com",
    "yelp": "https://www.yelp.com",
    "zillow": "https://www.zillow.com",
    "realtor": "https://www.realtor.com",
    "indeed": "https://www.indeed.com",
    "glassdoor": "https://www.glassdoor.com",
    "monster": "https://www.monster.com",
    "craigslist": "https://craigslist.org",
    "ebay": "https://www.ebay.com",
    "etsy": "https://www.etsy.com",
    "walmart": "https://www.walmart.com",
    "target": "https://www.target.com",
    "bestbuy": "https://www.bestbuy.com",
    "homedepot": "https://www.homedepot.com",
    "lowes": "https://www.lowes.com",
    "ikea": "https://www.ikea.com",
    "wayfair": "https://www.wayfair.com",
    "overstock": "https://www.overstock.com"
}

# === Open Item Function ===
def open_item(name):
    name = name.lower().strip()
    print(f"Trying to open: {name}")

    # First check system apps
    if name in system_apps:
        speak(f"Opening {name}")
        try:
            subprocess.Popen(system_apps[name], shell=True)
            return
        except Exception as e:
            print(f"Error opening system app: {e}")
            speak(f"Sorry, couldn't open {name}")

    # Check regular apps
    elif name in apps:
        speak(f"Opening {name}")
        try:
            os.system(f'start "" "{apps[name]}"')
            return
        except Exception as e:
            print(f"Error opening app: {e}")
            speak(f"Sorry, couldn't open {name}")

    # Check websites
    elif name in sites:
        speak(f"Opening {name}")
        webbrowser.open(sites[name])
        return

    # Partial matches
    else:
        # Check partial matches in system apps
        for sys_app, command in system_apps.items():
            if name in sys_app:
                speak(f"Opening {sys_app}")
                subprocess.Popen(command, shell=True)
                return
        
        # Check partial matches in regular apps
        for app_name, path in apps.items():
            if name in app_name:
                speak(f"Opening {app_name}")
                os.system(f'start "" "{path}"')
                return
        
        # Check partial matches in websites
        for site_name, url in sites.items():
            if name in site_name:
                speak(f"Opening {site_name}")
                webbrowser.open(url)
                return

    # If nothing found
    speak(f"Sorry, I couldn't find {name}.")

# === Close App Function ===
def close_app(app_name):
    app_name = app_name.lower().strip()
    print(f"Trying to close: {app_name}")

    # Find the process name from apps dictionary
    process_name = None
    
    # Exact match in apps
    if app_name in apps:
        process_name = apps[app_name]
        speak(f"Closing {app_name}")
    
    # Partial match in apps
    else:
        for app_key, app_exe in apps.items():
            if app_name in app_key:
                process_name = app_exe
                speak(f"Closing {app_key}")
                break
        else:
            # If not found in apps, try system apps
            if app_name in system_apps:
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
        print("Error closing app:", e)
        speak(f"Sorry, I couldn't close {app_name}")

def minimize_window(app_name=None):
    """Minimizes a window or the current one if no app specified."""
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
        print("Error minimizing window:", e)
        speak("I couldn't minimize that window.")


def maximize_window(app_name=None):
    """Maximizes a window or the current one if no app specified."""
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
        print("Error maximizing window:", e)
        speak("I couldn't maximize that window.")

def switch_app():
    """Switch to another app."""
    try:
        pyautogui.hotkey("alt", "tab")
        speak("Switched app.")
    except Exception as e:
        print("Error switching app:", e)
        speak("I couldn't switch the app.")

def is_chrome_running():
    """Check if Chrome browser is running."""
    for proc in psutil.process_iter(['name']):
        if 'chrome' in proc.info['name'].lower():
            return True
    return False

# === BROWSER CONTROL FUNCTIONS ===

def close_tab():
    """Close the current browser tab."""
    try:
        if is_chrome_running():
            pyautogui.hotkey("ctrl", "w")
            speak("Closed the tab.")
        else:
            speak("Chrome is not open, sir.")
    except Exception as e:
        print("Error closing tab:", e)
        speak("I couldn't close the tab.")


def new_tab():
    """Open a new browser tab."""
    try:
        if is_chrome_running():
            pyautogui.hotkey("ctrl", "t")
            speak("Opened a new tab.")
        else:
            speak("Chrome is not open, sir.")
    except Exception as e:
        print("Error opening new tab:", e)
        speak("I couldn't open a new tab.")


def next_tab():
    """Switch to the next browser tab."""
    try:
        if is_chrome_running():
            pyautogui.hotkey("ctrl", "tab")
            speak("Switched to the next tab.")
        else:
            speak("Chrome is not open, sir.")
    except Exception as e:
        print("Error switching tab:", e)
        speak("I couldn't switch to the next tab.")


def previous_tab():
    """Switch to the previous browser tab."""
    try:
        if is_chrome_running():
            pyautogui.hotkey("ctrl", "shift", "tab")
            speak("Switched to the previous tab.")
        else:
            speak("Chrome is not open, sir.")
    except Exception as e:
        print("Error switching to previous tab:", e)
        speak("I couldn't switch to the previous tab.")

# === Terminate Nexus ===
def terminate():
    global listening
    try:
        speak("Going to sleep. Goodbye!")
        listening = False
        pygame.mixer.quit()
    except Exception as e:
        print(f"Error while terminating: {e}")
    sys.exit(0)

def play_beep():
    winsound.Beep(1000, 500) 

# === Command Processor ===
def processCommand(c):
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
        speak("Shutting down your computer.")
        os.system("shutdown /s /t 5")
        return
    
    if "restart" in c:
        speak("Restarting your computer.")
        os.system("shutdown /r /t 5")
        return
    
    if "log out" in c:
        speak("Signing out.")
        os.system("shutdown /l")
        return

    # --- MISCELLANEOUS ---
    if "time" in c:
        speak(f"The time is {datetime.datetime.now().strftime('%I:%M %p')}")
        return
    
    if "date" in c:
        speak(f"Today is {datetime.datetime.now().strftime('%A, %d %B %Y')}")
        return
    
    if "screenshot" in c:
        filename = f"screenshot_{time.strftime('%Y%m%d-%H%M%S')}.png"
        pyautogui.screenshot(filename)
        speak(f"Screenshot saved as {filename}")
        return
    
    if "volume up" in c:
        pyautogui.press("volumeup")
        speak("Volume increased.")
        return
    
    if "volume down" in c:
        pyautogui.press("volumedown")
        speak("Volume decreased.")
        return
    
    if "mute" in c:
        pyautogui.press("volumemute")
        speak("Volume muted.")
        return
    
    if "battery" in c:
        battery = psutil.sensors_battery()
        speak(f"Battery is at {battery.percent} percent.")
        speak("Charging." if battery.power_plugged else "Not charging.")
        return
    
    if c.startswith("play "):
        song = c.replace("play ", "")
        speak(f"Playing {song} on YouTube")
        pywhatkit.playonyt(song)
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
        try:
            speak("Fetching top headlines.")
            url = f"https://newsapi.org/v2/top-headlines?country=pk&apiKey={newsapi}"
            r = requests.get(url)
            data = r.json().get("articles", [])[:5]
            for article in data:
                speak(article["title"])
        except Exception as e:
            print("News error:", e)
            speak("Could not fetch news.")
        return

    # --- TERMINATE ---
    if "sleep" in c or "goodbye" in c:
        terminate()
        return

    # --- FALLBACK ---
    speak("I didn't understand that. Please try again.")

# === LISTENERS ===
wake_word = "nexus"
awake = False
cooldown = 0.3

def callback(recognizer, audio):
    global awake, stop_flag, command_thread

    try:
        text = recognizer.recognize_google(audio).lower().strip()
        print(f"Heard: {text}")

        if not awake:
            # Detect wake word
            if wake_word in text:
                awake = True
                speak("Yes sir?")
                play_beep()
            time.sleep(cooldown)

        else:
            # Already awake — process command
            awake = False
            stop_flag = False
            command_thread = threading.Thread(target=processCommand, args=(text,))
            command_thread.start()

    except sr.UnknownValueError:
        pass
    except sr.RequestError:
        print("Speech recognition service error.")
    except Exception as e:
        print("Callback error:", e)


def start_background_listener():
    global listening
    speak("Initializing Nexus... System ready!")
    mic = sr.Microphone()

    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening in background... Say 'Nexus' to wake me.")

    stop_listening = recognizer.listen_in_background(mic, callback, phrase_time_limit=6)

    try:
        while listening:
            time.sleep(0.1)
    except KeyboardInterrupt:
        stop_listening(wait_for_stop=False)
        terminate()

# === MAIN ===
if __name__ == "__main__":
    start_background_listener()