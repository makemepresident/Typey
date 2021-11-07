from blessed import Terminal
from random import randint

#https://gist.github.com/deekayen/4148741#file-1-1000-txt
try:
    all_words = open('./assets/1-1000.txt').read().split()  # read all words in 1-1000.txt
except FileNotFoundError:
    exit('File not found')

MAX_LENGTH = 50

word_map = {}
for i in all_words:
    if len(i) not in word_map:
        word_map[len(i)] = []
    word_map[len(i)].append(i)

terminal = Terminal()

print(terminal.home + terminal.clear)

min_key = min(word_map.keys())
max_key = max(word_map.keys())

output = ""
for i in range(50):
    remaining_space = MAX_LENGTH - len(output)
    if(remaining_space > 0 and remaining_space < max_key):
        output += word_map[remaining_space][randint(1, len(word_map[remaining_space]) - 1)]
        print(terminal.center(terminal.black_on_darkkhaki(output)))
        output = ""
    length = randint(min_key, max_key)
    output += word_map[length][randint(0, len(word_map[length]) - 1)] + " "

while True:
    with terminal.cbreak(), terminal.hidden_cursor():
        inp = terminal.inkey()
    if(inp == terminal.KEY_ENTER):
        print(terminal.move_down(1))
    print(terminal.center(terminal.bold(inp), fillchar=""), end="")