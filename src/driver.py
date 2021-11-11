'''
* Responsible for retrieving word data from file
* Responsible for determining word length of test from input
* Responsible for determining the theme from input
* Responsible for starting and stopping game loop (automatic retries, generate new)
'''

import argparse

parser = argparse.ArgumentParser("Create a typing challenge for a certain amount of words")

parser.add_argument("--l", dest="length", default="25", help="Length of the typing test in words (10, 30, 50, or 100)")
parser.add_argument("--t", dest="theme", default="default", help="Typing test theme")

args = parser.parse_args()

all_words = open("./assets/1-1000.txt").read().split()  # read all words in 1-1000.txt