import random
from os import system, name

# list of all possible answers for the game
answers = []
with open('Answers.txt', 'r') as f:
    for line in f.readlines():
        answers.append(line.strip())

# list of all possible guesses and answers that make up valid inputs
valid_inputs = []
with open('AnswersAndGuesses.txt', 'r') as f:
    for line in f.readlines():
        valid_inputs.append(line.strip())


# Clears the console log based off of the operating system
def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux
    else:
        _ = system('clear')


# Resets and returns the colors of the onscreen keyboard back to its default values - white
def reset_keyboard_colors():
    kcolors = {'Q': 0, 'W': 0, 'E': 0, 'R': 0, 'T': 0, 'Y': 0, 'U': 0, 'I': 0, 'O': 0,
               'P': 0, 'A': 0, 'S': 0, 'D': 0, 'F': 0, 'G': 0, 'H': 0, 'J': 0, 'K': 0,
               'L': 0, 'Z': 0, 'X': 0, 'C': 0, 'V': 0, 'B': 0, 'N': 0, 'M': 0}
    return kcolors


# returns colored text based off of input RGB values.
def colored(r, g, b, text):
    return "\033[38;2;{};{};{}m{}\033[38;2;255;255;255m".format(r, g, b, text)


# Game class handles the current board info, input checking, and printing the board to the console.
def color_text(text, value):
    if value == 0:
        return colored(255, 255, 255, text)
    elif value == 1:
        return colored(100, 100, 100, text)
    elif value == 2:
        return colored(255, 255, 0, text)
    elif value == 3:
        return colored(0, 255, 0, text)


class game:

    def __init__(self):
        # Creates a board of 6 rows and 5 columns
        self.board = [["□" for i in range(5)] for i in range(6)]
        # Stores the current row index being used
        self.current_row = 0
        # Selects a random answer from answers, capitalizes it, and removes any newline characters
        self.answer = str(answers[random.randint(0, len(answers) - 1)]).upper().strip()
        # Create a dictionary that stores the color value of each letter
        self.keyboard_colors = reset_keyboard_colors()

    def reset_letter_frequency(self):
        letter_frequency = {}  # Stores each letter used in the answer as a key, and its frequency as the value
        # Loops through the answer, counting the number of times each letter is used
        for l in self.answer:
            if l in letter_frequency.keys():
                letter_frequency[l] += 1
            else:
                letter_frequency[l] = 1
        return letter_frequency

    def print_board(self):
        # Prints board
        for row in self.board:
            print("--", end="")
            for column in row:
                print(f" {column} ", end="")
            print("--")
        print("---Used Letters:---")
        i = 0
        for key in self.keyboard_colors.keys():
            if i == 10:
                print("")
                print("  ", end="")
            elif i == 19:
                print("")
                print("     ", end="")
            print(f"[{color_text(key, self.keyboard_colors[key])}]", end="")
            i += 1
        print("")

    def debug(self):
        print(f"{self.answer} {self.reset_letter_frequency()}")
        testarooney = reset_keyboard_colors()
        for key in testarooney.keys():
            print(f"{key} = {testarooney[key]}")

    def check_input(self, guess):
        guess = guess.upper().strip()
        letter_frequency = self.reset_letter_frequency()
        guess_colors = [1, 1, 1, 1, 1]  # 1 means no match, 2 means wrong spot, 3 means correct guess
        # Check to see if any letters of the guess are in the correct spot
        for i in range(5):
            # If the letter in the guess matches the letter in the answer, set the color of this guess to green and subtract one from the letters frequency
            if guess[i] == self.answer[i]:
                guess_colors[i] = 3
                self.keyboard_colors[guess[i]] = 3
                letter_frequency[guess[i]] -= 1
        for i, l in enumerate(guess):
            if guess_colors[i] != 3 and l in self.answer and letter_frequency[l] != 0:
                guess_colors[i] = 2
                if self.keyboard_colors[l] != 3:
                    self.keyboard_colors[l] = 2
                letter_frequency[l] -= 1
            elif self.keyboard_colors[guess[i]] == 0:
                self.keyboard_colors[guess[i]] = 1

        for i, l in enumerate(guess):
            self.board[self.current_row][i] = color_text(l, guess_colors[i])
        self.current_row += 1


def main():
    print(colored(255, 255, 255, ""), end="")  # sets all text to white (unless specified)
    test = game()
    test.print_board()
    while True:
        test.check_input(input("Input Word Moron"))
        test.print_board()


if __name__ == "__main__":
    main()
