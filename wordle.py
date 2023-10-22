import re
import random
from os import system, name

# list of all possible answers for the game
with open('Answers.txt', 'r') as f:
    answers = list(f)

# list of all possible guesses and answers that make up valid inputs
with open('AnswersAndGuesses.txt', 'r') as f:
    valid_inputs = list(f)


def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux
    else:
        _ = system('clear')


def reset_keyboard_colors():
    kcolors = {'Q': 0, 'W': 0, 'E': 0, 'R': 0, 'T': 0, 'Y': 0, 'U': 0, 'I': 0, 'O': 0,
               'P': 0, 'A': 0, 'S': 0, 'D': 0, 'F': 0, 'G': 0, 'H': 0, 'J': 0, 'K': 0,
               'L': 0, 'Z': 0, 'X': 0, 'C': 0, 'V': 0, 'B': 0, 'N': 0, 'M': 0}
    return kcolors


class game:

    def __init__(self):
        self.board = [["□" for i in range(5)] for i in range(6)]  # Creates a board of 6 rows and 5 columns
        self.current_row = 0  # Stores the current row index being used
        self.answer = str(answers[random.randint(0, len(answers) - 1)]).upper()  # Selects a random answer from answers
        self.letter_frequency = {}
        for l in self.answer:
            if l in self.letter_frequency.keys():
                self.letter_frequency[l] += 1
            elif l != '\n':
                self.letter_frequency[l] = 1


    def print_board(self):
        print(self.answer)
        print(self.letter_frequency)


if __name__ == "__main__":
    keyboard_colors = reset_keyboard_colors()
    test = game()
    test.print_board()
