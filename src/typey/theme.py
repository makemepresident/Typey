from blessed import Terminal
import json
import pkg_resources

class Theme:

    def __init__(self, name) -> None:
        terminal = Terminal()
        defaults = pkg_resources.resource_filename("typey", "defaults.json")
        res = pkg_resources.resource_filename("typey", "./assets/themes.json")
        try:
            file = open(res, "r")
            js = json.load(file)
            if name != "typey_default":
                self.complete = getattr(terminal, js[name]["c"])
                self.incomplete = getattr(terminal, js[name]["i"])
                self.backdrop = getattr(terminal, js[name]["b"])
                js["default"]["c"] = js[name]["c"]
                js["default"]["i"] = js[name]["i"]
                js["default"]["b"] = js[name]["b"]
            else:
                self.setTypeyDefault(terminal, js)
            if name != "default":
                try:
                    file = open(res, "w")
                    json.dump(js, file, indent=4)
                except:
                    raise Exception
        except Exception as e:
            self.setTypeyDefault(terminal)
    
    def setTypeyDefault(self, terminal, js=None):
        if js != None:
            js["default"]["c"] = "white_on_darkkhaki"
            js["default"]["i"] = "black_on_darkkhaki"
            js["default"]["b"] = "on_darkkhaki"
        self.complete = terminal.white_on_darkkhaki
        self.incomplete = terminal.black_on_darkkhaki
        self.backdrop = terminal.on_darkkhaki               