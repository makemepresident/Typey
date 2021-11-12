from blessed import Terminal
import json

class Theme:

    def __init__(self, name) -> None:
        terminal = Terminal()
        try:
            file = open("./assets/themes.json", "r")
            js = json.load(file)
            self.complete = getattr(terminal, js[name]["c"])
            self.incomplete = getattr(terminal, js[name]["i"])
            self.backdrop = getattr(terminal, js[name]["b"])
            if name != "default":
                js["default"]["c"] = js[name]["c"]
                js["default"]["i"] = js[name]["i"]
                js["default"]["b"] = js[name]["b"]
                try:
                    file = open("./assets/themes.json", "w")
                    json.dump(js, file)
                except:
                    raise Exception
        except Exception as e:
            self.setTyPyDefault(terminal)
    
    def setTyPyDefault(self, terminal):
        self.complete = terminal.white_on_darkkhaki
        self.incomplete = terminal.black_on_darkkhaki
        self.backdrop = terminal.on_darkkhaki