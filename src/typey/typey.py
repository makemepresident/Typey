'''
* Responsible for retrieving word data from file
* Responsible for determining word length of test from input
* Responsible for determining the theme from input
* Responsible for starting and stopping game loop (automatic retries, generate new)
'''
from blessed import Terminal
# from .challenge import Challenge
# from .theme import Theme
from challenge import Challenge
from filecontroller import FileController
import argparse

def main():
    defaults = FileController.getDefaults()
    parser = argparse.ArgumentParser("Create quick, repeatable, regenerative typing tests in your terminal.")
    parser.add_argument("--l", "--length", dest="length", default=defaults["default_length"], help="Length of the typing test in words.")
    parser.add_argument("--t", "--theme", dest="theme", default=defaults["default_theme"], help="Temporarily changes the theme of the typing test; use --dt to set a default theme")
    parser.add_argument("--dt", "--default_theme", dest="default_theme", action="store_true", help="Set a new default theme defined in themes.json.")
    parser.add_argument("--dl", "--default_length", dest="default_length", action="store_true", help="Set a new default length.")
    parser.add_argument("--at", "--add_theme", dest="add_theme", action="store_true", help="Add a new theme to themes.json in the form: \"name,completed,incomplete,backdrop\"")
    parser.add_argument("--lt", "--list_themes", dest="list_themes", action="store_true", help="List all themes available for Typey.")
    parser.add_argument("--d", "--defaults", dest="defaults", action="store_true", help="Reset to Typey defaults.")
    args = parser.parse_args()

    if int(args.length) > 100:
        args.length = 100
    elif int(args.length) < 1:
        args.length = 1

    option_changed = False
    if args.default_theme:
        try:
            FileController.setNewDefaultTheme(args.default_theme)
            option_changed = True
        except Exception as e:
            print(e.args)

    if args.default_length:
        try:
            FileController.setNewDefaultLength(args.default_length)
            option_changed = True
        except Exception as e:
            print(e.args)

    if args.add_theme:
        try:
            FileController.addNewTheme(args.add_theme)
            option_changed = True
        except Exception as e:
            print(e.args)

    if args.list_themes:
        try:
            FileController.listThemes()
            option_changed = True
        except Exception as e:
            print(e.args)

    if args.defaults:
        try:
            FileController.setNewDefaultLength(25)
            FileController.setNewDefaultTheme("typey_default")
            option_changed = True
        except Exception as e:
            print(e.args)

    if not option_changed:
        terminal = Terminal()
        theme = FileController(args.theme)
        challenge = Challenge(args.length, theme, terminal)
        all_words = FileController.getWords()  # read all words in 1-1000.txt
        reset = False

        while True:
            with terminal.fullscreen():
                if not reset:
                    challenge.generate_challenge(all_words)
                else:
                    challenge.reset()
                reset = True
                if challenge.main_loop():
                    characters, words = challenge.evaluate_accuracy()
                    raw_wpm = str((challenge.length * 60) / (challenge.final_time - challenge.initial_time))
                    wpm = str((words * 60) / (challenge.final_time - challenge.initial_time))
                    cpm = str(characters * 60 / (challenge.final_time - challenge.initial_time))
                    print(terminal.home + terminal.clear + terminal.move_y(terminal.height // 2) + theme.incomplete(terminal.center(raw_wpm[:raw_wpm.index(".") + 2] + " RAW; " + wpm[:wpm.index(".") + 2] + " WPM; " + cpm[:cpm.index(".") + 2] + " CPM")))
                    print(theme.incomplete(terminal.center("Press tab to start a new challenge; press any other key to try the same challenge again...")))
                    with terminal.cbreak(), terminal.hidden_cursor():
                        inp = terminal.inkey()
                        if inp.code == terminal.KEY_TAB:
                            reset = False
                        elif inp.code == terminal.KEY_ESCAPE:
                            print(terminal.home + terminal.clear)
                            exit()
                else:
                    exit()
    else:
        exit()

main()