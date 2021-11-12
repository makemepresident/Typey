from blessed import Terminal
import json

class Theme:

    def __init__(self, name) -> None:
        terminal = Terminal()
        try:
            file = open("../assets/themes.json")
            js = json.load(file)
            self.complete = getattr(terminal, js[name]["c"])
            self.incomplete = getattr(terminal, js[name]["i"])
            self.backdrop = getattr(terminal, js[name]["b"])
        except Exception as e:
            print("Failed to correctly load themes; termminal will run with OS default")
            print(e)