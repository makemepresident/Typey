from random import randint
import time

class Challenge:

    def __init__(self, length, theme, terminal, all_words) -> None:
        self.terminal = terminal
        self.length = int(length)
        self.theme = theme
        self.all_words = all_words
        self.has_reset = False
        self.cutoff_indices = set()
        self.no_render = False

    def generate_challenge(self):
        self.initial_time = None
        self.finished = False
        self.stack = []
        self.evaluation_stack = []
        for i in range(self.length):
            word = self.all_words[randint(0, len(self.all_words) - 1)]
            for letter in word:
                self.stack.append(letter)
            if i != self.length - 1:
                self.stack.append(" ")
        self.reset_stack = self.stack.copy()

    def reset(self):
        self.initial_time = None
        self.finished = False
        self.has_reset = True
        self.stack = self.reset_stack.copy()
        self.evaluation_stack = []
        self.no_render = False

    def render(self, current_stack):
        lines_rendered = 0 # visible lines in terminal
        final = "" # distinct from output for centering/aesthetics
        output = ""
        width_check = 0 # ensures that a word does not get split between lines
        padded_width = self.terminal.width - (self.terminal.width // 3) # aesthetic centering
        for i in range(len(self.stack)):
            width_check += 1
            if (width_check > padded_width or width_check > 100) and self.stack[i] == " ": # if words at width limit and current item is a space (space sends to next line)
                final += self.theme.backdrop(self.terminal.center(output))
                output = ""
                width_check = 0
                self.cutoff_indices.add(i) # add end of line index for deletion check
                lines_rendered += 1
                if lines_rendered == 3: # compact lines rendered due to performance issues
                    break
            if i < len(current_stack): # current element must be a letter that was written or incorrect
                if not self.no_render and i in self.cutoff_indices:
                    '''
                    Due to performance reasons, the rendering algorithm has to be "smart".
                    3 lines are rendered at a time and the indices of the effective \n is
                    recorded. When an index is reached, we checked to see if the finish
                    flag has been set (no_render) and if not, we remove the completed
                    portion of the stack and its corresponding cutoff index from the 
                    global set. The current stack is cleared (as it must have matched)
                    and render is called recursively to update the first line graphically.
                    '''
                    self.stack = self.stack[i + 1:]
                    self.cutoff_indices.remove(i)
                    self.evaluation_stack += current_stack
                    current_stack.clear()
                    return self.render(current_stack)
                if self.stack[i] == current_stack[i]: # letter is correct
                    output += self.theme.complete(self.stack[i])
                else:
                    output += self.terminal.on_red(self.stack[i]) # incorrect
                if i == len(self.stack) - 1: # finish challenge
                    self.finished = True
                    self.evaluation_stack += current_stack
            else:
                output += self.theme.incomplete(self.stack[i]) # normal lettering (not yet reached)
        # two cases as final output gets concatenated and no_render needs to be thrown so all lines do not get deleted at end of challenge
        if lines_rendered == 3:
            return final
        else:
            self.no_render = True
            return final + self.theme.backdrop(self.terminal.center(output))

    def evaluate_accuracy(self):
        incorrect_words = 0
        incorrect_characters = 0
        err = False
        for i in range(len(self.reset_stack)):
            if self.reset_stack[i] == " " or i == len(self.reset_stack) - 1:
                if err:
                    incorrect_words += 1
                err = False
            if self.reset_stack[i] != self.evaluation_stack[i]:
                incorrect_characters += 1
                err = True
        return len(self.stack) - incorrect_characters, self.length - incorrect_words

    def main_loop(self):
        redraw = self.terminal.home + self.terminal.clear
        with self.terminal.cbreak(), self.terminal.hidden_cursor():
            if not self.has_reset:
                print(self.terminal.home + self.terminal.clear + self.terminal.move_y(self.terminal.height // 2))
                print(self.theme.incomplete(self.terminal.center(str(self.length) + " word challenge generated:")))
                print(self.theme.incomplete(self.terminal.center("Press ESC at any time to exit; press TAB at any time to reset and generate a new challenge; press any key to continue...")))
                inp = self.terminal.inkey()
                if inp.code == self.terminal.KEY_ESCAPE:
                    return False
            current_stack = []
            while True:
                print(redraw + self.terminal.move_y(self.terminal.height // 2) + self.render(current_stack))
                if self.finished:
                    self.final_time = time.time()
                    self.has_reset = True
                    return True
                inp = self.terminal.inkey()
                if self.initial_time == None:
                    self.initial_time = time.time()
                if inp.code == self.terminal.KEY_BACKSPACE:
                    if len(current_stack) != 0:
                        del current_stack[-1]
                elif inp.code == self.terminal.KEY_ESCAPE:
                    return False
                elif inp.code == self.terminal.KEY_TAB:
                    self.generate_challenge()
                    current_stack = []
                else:
                    current_stack.append(inp)