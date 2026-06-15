import webbrowser
from utils.helpers import load_config, get_arg

config = load_config()

def open_site(args):
    site = get_arg(args, 0)

    if site == "github" or site == "GitHub":
        webbrowser.open(config["browser"]["github"])
        return "Opening GitHub"
    
    if site == "google" or site == "Google":
        webbrowser.open(config["browser"]["google"])
        return "Opening Google"

    if site == "youtube" or site == "YouTube":
        webbrowser.open(config["browser"]["youtube"])
        return "Opening YouTube"

    return "Unknown site"


def register(registry):
    registry.register("open", open_site)