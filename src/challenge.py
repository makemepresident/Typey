from blessed import Terminal
from random import randint
import time

class Challenge:

    def __init__(self, length, theme) -> None:
        self.terminal = Terminal()
        self.length = int(length)
        self.theme = theme

    def generate_challenge(self, word_list):
        self.pointer = 0
        self.initial_time = None
        self.stack = []
        for i in range(self.length):
            word = word_list[randint(0, len(word_list) - 1)]
            for letter in word:
                self.stack.append(letter)
            if i != self.length - 1:
                self.stack.append(" ")

    def press(self, current_stack):
        self.pointer = 0
        for i in range(len(current_stack)):
            if self.stack[i] == current_stack[i]:
                self.pointer += 1

    def render(self, current_stack):
        self.press(current_stack)
        final = ""
        output = ""
        width_check = 0
        for index, value in enumerate(self.stack):
            width_check += 1
            if width_check > self.terminal.width - (self.terminal.width // 2) and value == " ":
                final += self.theme.backdrop(self.terminal.center(output))
                output = ""
                width_check = 0
            if index < self.pointer:
                output += self.theme.complete(value)
            elif index < len(current_stack):
                output += self.terminal.on_red(value)
            else:
                output += self.theme.incomplete(value)
        return final + self.theme.backdrop(self.terminal.center(output))

    def finish(self):
        if self.pointer == len(self.stack):
            return True
        return False

    def main_loop(self):
        self.terminal.enter_fullscreen
        redraw = self.terminal.home + self.terminal.clear
        with self.terminal.cbreak(), self.terminal.hidden_cursor():
            print(self.terminal.home + self.terminal.clear + self.terminal.move_y(self.terminal.height // 2))
            print(self.theme.incomplete(self.terminal.center(str(self.length) + " word challenge generated; press any key to continue...")))
            inp = self.terminal.inkey()
            print(redraw)
            current_stack = []
            while True:
                print(redraw + self.render(current_stack))
                if self.finish():
                    self.final_time = time.time()
                    words_per_minute = (self.length * 60) // (self.final_time - self.initial_time)
                    print(self.theme.incomplete(self.terminal.center("Finished! Recorded " + str(words_per_minute))))
                    break
                inp = self.terminal.inkey()
                if self.initial_time == None:
                    self.initial_time = time.time()
                if inp.code == self.terminal.KEY_BACKSPACE:
                    if len(current_stack) != 0:
                        del current_stack[-1]
                else:
                    current_stack.append(inp)
                # self.press(current_stack)