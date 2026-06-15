from core.registry import CommandRegistry

class Engine:
    def __init__(self):
        self.registry = CommandRegistry()

    def load_plugins(self):
        import plugins.system
        import plugins.web

        plugins.system.register(self.registry)
        plugins.web.register(self.registry)

    def run(self):
        while True:
            user_input = input(">> ").strip()

            if user_input.lower() == "exit":
                print("Exiting...")
                break

            if not user_input:
                continue

            parts = user_input.split()
            command = parts[0]
            args = parts[1:] if len(parts) > 1 else []

            result = self.registry.execute(command, args)
            print(result)