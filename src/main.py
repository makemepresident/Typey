from blessed import Terminal
from random import randint
import time

# https://gist.github.com/deekayen/4148741#file-1-1000-txt
all_words = open("./assets/1-1000.txt").read().split()  # read all words in 1-1000.txt
MAX_LENGTH = 50

class Challenge:

    def __init__(self, length, complete, incomplete) -> None:
        self.pointer = 0
        self.words = self.generate_challenge(length)
        self.complete = complete
        self.incomplete = incomplete

    def generate_challenge(self, length):
        words = []
        for i in range(length):
            words.append(all_words[randint(0, len(all_words) - 1)])
        return words

    def press(self, word):
        if word == self.words[self.pointer]:
            self.pointer += 1
            return True
        return False

    def render(self, line_word_limit):
        output = ""
        for ind, val in enumerate(self.words):
            if ind % line_word_limit == 0:
                output += "\n"
            if ind < self.pointer:
                output += self.complete(val)
            else:
                output += self.incomplete(val)
            if ind == len(self.words) - 1:
                break
            else:
                output += self.incomplete(" ")
        return output

    def finish(self):
        if self.pointer == len(self.words):
            return True
        return False

# def generate_word_map():
#     word_map = {}
#     for i in all_words:
#         if len(i) not in word_map:
#             word_map[len(i)] = []
#         word_map[len(i)].append(i)
#     return word_map

def generate_word(stack):
    output = ""
    for i in stack:
        output += i
    return output.strip()

LENGTH = 5
LINE_WORD_LIMIT = 10

terminal = Terminal()
complete = terminal.blue_on_darkkhaki
incomplete = terminal.black_on_darkkhaki
challenge = Challenge(LENGTH, complete, incomplete)

print(terminal.home + terminal.clear + terminal.move_y(terminal.height // 2))
print(terminal.black_on_darkkhaki(terminal.center(str(LENGTH) + " word challenge generated; press any key to continue...")))

initial_time = None
final_time = None

with terminal.cbreak(), terminal.hidden_cursor():
    inp = terminal.inkey()
    print(terminal.home + terminal.clear)
    stack = []
    while True:
        print(terminal.clear + terminal.center(challenge.render(LINE_WORD_LIMIT)))
        print(terminal.move_down(1) + generate_word(stack))
        if challenge.finish():
            final_time = time.time()
            words_per_minute = (LENGTH * 60) // (final_time - initial_time)
            print(terminal.move_down(1) + terminal.center(incomplete("Finished! Recorded " + str(words_per_minute))))
            break
        inp = terminal.inkey()
        if initial_time == None:
            initial_time = time.time()
        if inp.code == terminal.KEY_BACKSPACE:
            if len(stack) != 0:
                del stack[-1]
        else:
            stack.append(inp)
        if challenge.press(generate_word(stack)):
            stack = []


# min_key = min(word_map.keys())
# max_key = max(word_map.keys())

# output = ""
# for i in range(50):
#     remaining_space = MAX_LENGTH - len(output)
#     if(remaining_space > 0 and remaining_space < max_key):
#         output += word_map[remaining_space][randint(1, len(word_map[remaining_space]) - 1)]
#         print(terminal.center(terminal.black_on_darkkhaki(output)))
#         output = ""
#     length = randint(min_key, max_key)
#     output += word_map[length][randint(0, len(word_map[length]) - 1)] + " "

# stack = []
# terminal.move_down(1)
# written = ""
# while True:
#     with terminal.cbreak(), terminal.hidden_cursor():
#         inp = terminal.inkey()
#     if(inp == terminal.KEY_ENTER): # change handling to assert word, check if correct (on space too)
#         print(terminal.move_down(1))
#     print(terminal.move_up(1) + terminal.clear_eol + terminal.move_up(1))
#     if(inp == terminal.KEY_BACKSPACE or inp == terminal.KEY_DELETE):
#         written = stack[-1]
#         del stack[-1]
#     else:
#         written += terminal.bold(inp)
#     stack.append(written)
#     print(terminal.center(written))