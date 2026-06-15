class CommandRegistry:
    def __init__(self):
        self.commands = {}

    def register(self, name, func):
        self.commands[name] = func

    def execute(self, name, args = None):
        if name in self.commands:
            return self.commands[name](args)
        else:
            return f" Command '{name}' not Found! "