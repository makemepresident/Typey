from blessed import Terminal
import json

class Theme:

    def __init__(self, name) -> None:
        terminal = Terminal()
        try:
            file = open("./assets/themes.json", "r")
            js = json.load(file)
            if name != "typy_default":
                self.complete = getattr(terminal, js[name]["c"])
                self.incomplete = getattr(terminal, js[name]["i"])
                self.backdrop = getattr(terminal, js[name]["b"])
                js["default"]["c"] = js[name]["c"]
                js["default"]["i"] = js[name]["i"]
                js["default"]["b"] = js[name]["b"]
            else:
                self.setTyPyDefault(terminal, js)
            if name != "default":
                
                try:
                    file = open("./assets/themes.json", "w")
                    json.dump(js, file, indent=4)
                except:
                    raise Exception
        except Exception as e:
            self.setTyPyDefault(terminal)
    
    def setTyPyDefault(self, terminal, js=None):
        if js != None:
            js["default"]["c"] = "white_on_darkkhaki"
            js["default"]["i"] = "black_on_darkkhaki"
            js["default"]["b"] = "on_darkkhaki"
        self.complete = terminal.white_on_darkkhaki
        self.incomplete = terminal.black_on_darkkhaki
        self.backdrop = terminal.on_darkkhaki               