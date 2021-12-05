'''
* Responsible for retrieving word data from file
* Responsible for determining word length of test from input
* Responsible for determining the theme from input
* Responsible for starting and stopping game loop (automatic retries, generate new)
'''
from blessed import Terminal
from .challenge import Challenge
from .theme import Theme
import argparse
import pkg_resources
import json

def main():
    defaults = json.load(pkg_resources.resource_string('typey', 'defaults.json'))
    

    parser = argparse.ArgumentParser("Create quick, repeatable, regenerative typing tests in your terminal.")
    parser.add_argument("--l", dest="length", default=defaults["default_length"], help="Length of the typing test in words. Has an upper limit of 50 due to rendering issues** DEFAULT=25")
    parser.add_argument("--t", dest="theme", default=defaults["default_theme"], help="Colour theme of the terminal; changing this will set a new default in JSON. Try \"typey_default\" to reset the terminal back to the original theme. DEFAULT=on_darkkhaki")
    args = parser.parse_args()

    if int(args.length) > 50:
        args.length = 50
    elif int(args.length) < 1:
        args.length = 1

    terminal = Terminal()
    theme = Theme(args.theme)
    challenge = Challenge(args.length, theme, terminal)
    res = pkg_resources.resource_filename("typey", "./assets/1-1000.txt")
    all_words = open(res).read().split()  # read all words in 1-1000.txt
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