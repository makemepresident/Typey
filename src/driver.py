'''
* Responsible for retrieving word data from file
* Responsible for determining word length of test from input
* Responsible for determining the theme from input
* Responsible for starting and stopping game loop (automatic retries, generate new)
'''
from blessed import Terminal
from challenge import Challenge
from theme import Theme
import argparse

parser = argparse.ArgumentParser("Create a typing challenge for a certain amount of words")

parser.add_argument("--l", dest="length", default="25", help="Length of the typing test in words (10, 30, 50, or 100)")
parser.add_argument("--t", dest="theme", default="default", help="Typing test theme")

args = parser.parse_args()

terminal = Terminal()
challenge = Challenge(args.length, Theme(args.theme), terminal)
all_words = open("../assets/1-1000.txt").read().split()  # read all words in 1-1000.txt
reset = False

while True:
    if not reset:
        challenge.generate_challenge(all_words)
    else:
        challenge.reset()
    reset = True
    challenge.main_loop()
    with terminal.cbreak(), terminal.hidden_cursor():
        inp = terminal.inkey()
        if inp.code == terminal.KEY_TAB:
            reset = False
        elif inp.code == terminal.KEY_ESCAPE:
            print(terminal.home + terminal.clear)
            exit()