import yaml

def load_config():
    """Load YAML configuration file"""
    with open("D:\Git Repository\PyFusion\CLI\config.yaml", "r") as file:
        return yaml.safe_load(file)


def get_arg(args, index, default=None):
    """Safely get argument from args list"""
    try:
        return args[index]
    except IndexError:
        return default


def log(message):
    """Simple logger"""
    print(f"[LOG] {message}")