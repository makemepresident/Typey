'''
* Responsible for retrieving word data from file
* Responsible for determining word length of test from input
* Responsible for determining the theme from input
* Responsible for starting and stopping game loop (automatic retries, generate new)
'''
from blessed import Terminal
from .challenge import Challenge
from .filecontroller import FileController
# from challenge import Challenge
# from filecontroller import FileController
import argparse

def init_parser():
    defaults = FileController.getDefaults()
    parser = argparse.ArgumentParser("Create quick, repeatable, regenerative typing tests in your terminal.")
    parser.add_argument("--l", "--length", dest="length", default=defaults["default_length"], help="Length of the typing test in words.")
    parser.add_argument("--t", "--theme", dest="theme", default=defaults["default_theme"], help="Temporarily changes the theme of the typing test; use --dt to set a default theme")
    parser.add_argument("--dt", "--default_theme", dest="default_theme", help="Set a new default theme defined in themes.json.")
    parser.add_argument("--dl", "--default_length", dest="default_length", help="Set a new default length.")
    parser.add_argument("--at", "--add_theme", dest="add_theme", help="Add a new theme to themes.json in the form: \"name,completed,incomplete,backdrop\" from https://blessed.readthedocs.io/en/latest/colors.html")
    parser.add_argument("--lt", "--list_themes", dest="list_themes", action="store_true", help="List all themes available for Typey.")
    parser.add_argument("--d", "--defaults", dest="defaults", help="Reset to Typey defaults.")
    return parser

def handle_args(args):
    '''
    Used to deal with terminal arguments pertaining to modifying settings or adding and viewing themes
    '''
    # constrain length
    if int(args.length) > 1000:
        args.length = 1000
    elif int(args.length) < 1:
        args.length = 1
    option_changed = False
    try:
        if args.default_theme:
            FileController.setNewDefaultTheme(args.default_theme)
            option_changed = True
        if args.default_length:
            FileController.setNewDefaultLength(args.default_length)
            option_changed = True
        if args.add_theme:
            FileController.addTheme(Terminal(), *args.add_theme.split(","))
            option_changed = True
        if args.list_themes:
            FileController.listThemes()
            option_changed = True
        if args.defaults:
            FileController.setNewDefaultLength(25)
            FileController.setNewDefaultTheme("typey_default")
            option_changed = True
        if option_changed:
            exit()
    except Exception as e:
        exit(e.args)

def calculate_rates(length, final_time, initial_time, words, characters):
    raw_wpm = str((length * 60) / (final_time - initial_time))
    wpm = str((words * 60) / (final_time - initial_time))
    cpm = str(characters * 60 / (final_time - initial_time))
    return raw_wpm, wpm, cpm

def main():
    args = init_parser().parse_args()
    handle_args(args)
    terminal = Terminal() # init main terminal
    theme = FileController.getTheme(terminal, args.theme)
    all_words = FileController.getWords()  # read all words in 1-1000.txt
    challenge = Challenge(args.length, theme, terminal, all_words)
    reset = False
    while True:
        with terminal.fullscreen():
            if not reset:
                challenge.generate_challenge()
            else:
                challenge.reset()
            reset = True
            if challenge.main_loop():
                characters, words = challenge.evaluate_accuracy()
                raw_wpm, wpm, cpm = calculate_rates(challenge.length, challenge.final_time, challenge.initial_time, words, characters)
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

main()