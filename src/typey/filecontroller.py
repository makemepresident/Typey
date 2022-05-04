import json
import os
import pkg_resources
from types import SimpleNamespace

class FileController:

    # themes_path = pkg_resources.resource_filename("typey", "./assets/themes.json")
    # defaults_path = pkg_resources.resource_filename("typey", "./assets/defaults.json")
    # words_path = pkg_resources.resource_filename("typey", "./assets/1-1000.txt")
    themes_path = './src/typey/assets/themes.json'
    defaults_path = './src/typey/assets/config.json'
    words_path = './src/typey/assets/1-1000.txt'

    @staticmethod
    def listThemes():
        with open(FileController.themes_path, 'r') as f:
            themes = json.load(f)
            for theme in themes:
                print(theme)

    @staticmethod
    def getWords():
        with open(FileController.words_path, 'r') as f:
            words = f.read().splitlines()
            return words

    @staticmethod
    def getDefaults():
        with open(FileController.defaults_path) as f:
            return json.load(f)

    @staticmethod
    def getTheme(terminal, name) -> None:
        try:
            js = json.load(open(FileController.themes_path, "r"))
            if name in js:
                return SimpleNamespace(**{"complete": getattr(terminal, js[name]["c"]), "incomplete": getattr(terminal, js[name]["i"]), "backdrop": getattr(terminal, js[name]["b"])})
        except:
            return SimpleNamespace(**{"complete": terminal.white_on_darkkhaki, "incomplete": terminal.black_on_darkkhaki, "backdrop": terminal.on_darkkhaki})

    @staticmethod
    def addTheme(terminal, name, complete, incomplete, backdrop):
        js = json.load(open(FileController.themes_path, "r"))
        if hasattr(terminal, complete) and hasattr(terminal, incomplete) and hasattr(terminal, backdrop):
            js[name] = {"c": complete, "i": incomplete, "b": backdrop}
            json.dump(js, open(FileController.themes_path, "w"), indent=4)
        else:
            raise Exception("Unable to find terminal colors")


    @staticmethod
    def setNewDefaultTheme(theme_name):
        '''
        Load the defaults file
        Load the themes file
        Check if the theme exists
        If it does, set the default theme value in the defaults file to the theme name
        '''
        themes_js = json.load(open(FileController.themes_path, "r"))
        if theme_name in themes_js:
            defaults_js = json.load(open(FileController.defaults_path, "r"))
            defaults_js["default_theme"] = theme_name
            json.dump(defaults_js, open(FileController.defaults_path, "w"), indent=4)
        else:
            raise Exception("Theme not found in themes.json")

    @staticmethod
    def setNewDefaultLength(length):
        if isinstance(length, int) and length > 0 and length < 100:
            defaults_file = open(FileController.defaults_path, "r+")
            defaults_js = json.load(defaults_file)
            defaults_js["default_length"] = length
            json.dump(defaults_js, defaults_file, indent=4)
        else:
            raise Exception("Length must be an integer between 0 and 100")