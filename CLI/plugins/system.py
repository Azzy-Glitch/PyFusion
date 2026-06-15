import datetime

def time_command(args):
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def register(registry):
    registry.register("time", time_command)