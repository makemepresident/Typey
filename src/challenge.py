from blessed import Terminal
from random import randint
import time

class Challenge:

    def __init__(self, theme) -> None:
        self.terminal = Terminal()
        self.theme = theme

    def generate_challenge(self, word_list, length):
        self.stack = []
        for i in range(length):
            word = word_list[randint(0, len(word_list) - 1)]
            for letter in word:
                stack.append(letter)
            if i != length - 1:
                stack.append(" ")

    def press(self, current_stack):
        self.pointer = 0
        for i in range(len(current_stack)):
            if self.stack[i] == current_stack[i]:
                self.pointer += 1

    def render(self):
        output = ""
        for index, value in enumerate(self.stac):
            if index =< self.pointer:
                output += self.theme.complete(value)
            else:
                output += self.incomplete(val)
            # if ind == len(self.words) - 1:
            #     break
            # else:
            #     output += self.incomplete(" ")
        return output

    def finish(self):
        if self.pointer == len(self.letter_stack):
            return True
        return False

def generate_word(stack):
    output = ""
    for i in stack:
        output += i
    return output.strip()

LENGTH = 25
LINE_WORD_LIMIT = 10

terminal = Terminal()
backdrop = ""
redraw = terminal.home + backdrop + terminal.clear
complete = terminal.white_on_darkkhaki
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
        print(redraw + challenge.render(LINE_WORD_LIMIT))
        # print(redraw + challenge.render(LINE_WORD_LIMIT))
        # print(terminal.move_down(1) + complete(generate_word(stack)))
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
        challenge.press(stack)