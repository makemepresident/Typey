from blessed import Terminal
from random import randint
import time

class Challenge:

    def __init__(self, length, theme, terminal) -> None:
        self.terminal = terminal
        self.length = int(length)
        self.theme = theme

    def generate_challenge(self, word_list):
        self.initial_time = None
        self.finished = False
        self.has_reset = False
        self.stack = []
        for i in range(self.length):
            word = word_list[randint(0, len(word_list) - 1)]
            for letter in word:
                self.stack.append(letter)
            if i != self.length - 1:
                self.stack.append(" ")

    def reset(self):
        self.initial_time = None
        self.finished = False
        self.has_reset = True

    def render(self, current_stack):
        final = ""
        output = ""
        width_check = 0
        for i in range(len(self.stack)):
            width_check += 1
            if width_check > self.terminal.width - (self.terminal.width // 3) and self.stack[i] == " ":
                final += self.theme.backdrop(self.terminal.center(output))
                output = ""
                width_check = 0
            if i < len(current_stack):
                if self.stack[i] == current_stack[i]:
                    output += self.theme.complete(self.stack[i])
                    if i == len(self.stack) - 1:
                        self.finished = True
                else:
                    output += self.terminal.on_red(self.stack[i])
            else:
                output += self.theme.incomplete(self.stack[i])
        return final + self.theme.backdrop(self.terminal.center(output))

    def evaluate_accuracy(self, final_stack):
        incorrect_words = 0
        for i in range(len(self.stack)):
            if self.stack[i] == " ":
                if err:
                    incorrect_words += 1
                err = False
                continue
            if self.stack[i] != final_stack[i]:
                err = True

    def main_loop(self):
        redraw = self.terminal.home + self.terminal.clear
        with self.terminal.cbreak(), self.terminal.hidden_cursor():
            if not self.has_reset:
                print(self.terminal.home + self.terminal.clear + self.terminal.move_y(self.terminal.height // 2))
                print(self.theme.incomplete(self.terminal.center(str(self.length) + " word challenge generated; press any key to continue; press ESC twice at any time to exit...")))
                inp = self.terminal.inkey()
                if inp.code == self.terminal.KEY_ESCAPE:
                    return
            current_stack = []
            while True:
                print(redraw + self.terminal.move_y(self.terminal.height // 2) + self.render(current_stack))
                if self.finished:
                    self.final_time = time.time()
                    # accuracy = self.evaluate_accuracy(current_stack)
                    words_per_minute = str((self.length * 60) / (self.final_time - self.initial_time))
                    print(redraw + self.terminal.move_y(self.terminal.height // 2) + self.theme.incomplete(self.terminal.center(words_per_minute[:words_per_minute.index(".") + 2] + " WPM")))
                    print(self.theme.incomplete(self.terminal.center("Press tab to start a new challenge; press any other key to try the same challenge again...")))
                    break
                inp = self.terminal.inkey()
                if self.initial_time == None:
                    self.initial_time = time.time()
                if inp.code == self.terminal.KEY_BACKSPACE:
                    if len(current_stack) != 0:
                        del current_stack[-1]
                elif inp.code == self.terminal.KEY_ESCAPE:
                    return
                else:
                    current_stack.append(inp)