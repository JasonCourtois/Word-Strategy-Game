import random
from os import system, name

# list of all possible answers for the game
answers = []
with open('Answers.txt', 'r') as f:
    for line in f.readlines():
        answers.append(line.strip().upper())

# list of all possible guesses and answers that make up valid inputs
valid_inputs = []
with open('AnswersAndGuesses.txt', 'r') as f:
    for line in f.readlines():
        valid_inputs.append(line.strip().upper())


# Clears the console log based off of the operating system
def clear():
    if name == 'nt':        # for windows
        _ = system('cls')
    else:                   # for mac and linux
        _ = system('clear')


# Resets and returns the colors of the onscreen keyboard back to its default values - white
def reset_keyboard_colors():
    keyboard_colors = {'Q': 0, 'W': 0, 'E': 0, 'R': 0, 'T': 0, 'Y': 0, 'U': 0, 'I': 0, 'O': 0,
                       'P': 0, 'A': 0, 'S': 0, 'D': 0, 'F': 0, 'G': 0, 'H': 0, 'J': 0, 'K': 0,
                       'L': 0, 'Z': 0, 'X': 0, 'C': 0, 'V': 0, 'B': 0, 'N': 0, 'M': 0}
    return keyboard_colors


# returns colored text based off of input RGB values.
def colored(r, g, b, text):
    return "\033[38;2;{};{};{}m{}\033[38;2;255;255;255m".format(r, g, b, text)


# Game class handles the current board info, input checking, and printing the board to the console.
def color_text(text, value):
    # 0 = Unchecked, so it should be white by default
    # 1 = Letter isn't used in answer, so it should be grey.
    # 2 = In the wrong spot, so it should be yellow.
    # 3 = in the right spot, so it should be green.
    if value == 0:
        return colored(255, 255, 255, text)
    elif value == 1:
        return colored(100, 100, 100, text)
    elif value == 2:
        return colored(255, 255, 0, text)
    elif value == 3:
        return colored(0, 255, 0, text)
    else:  # Catches any errors where there was an incorrect value inserted.
        return colored(255, 0, 0, "Error, wrong value inserted")


class Game:
    def __init__(self):
        self.board = [["□" for i in range(5)] for i in range(6)]    # Creates a board of 6 rows and 5 columns
        self.current_row = 0                                        # Stores the current row index being used
        self.answer = answers[random.randint(0, len(answers) - 1)]  # Selects a random answer from answers, capitalizes it, and removes any newline characters
        self.keyboard_colors = reset_keyboard_colors()              # Create a dictionary that stores the color value of each letter

    # Resets the dictionary that stores frequency of each letter in the answer.
    # This dictionary is used to tell how many yellow and green character should be assigned in any given guess.
    def reset_letter_frequency(self):
        letter_frequency = {}
        for letter in self.answer:                 # Loops through the answer, counting the number of times each letter is used
            if letter in letter_frequency.keys():
                letter_frequency[letter] += 1
            else:
                letter_frequency[letter] = 1
        return letter_frequency

    # Prints the game board to the console, followed by the on-screen keyboard of used keys.
    def print_board(self):
        for row in self.board:  # Prints each row with starting and ending dashes for style.
            print("--", end="")
            for column in row:
                print(f" {column} ", end="")
            print("--")

        print("---Used Letters:---")
        i = 0  # Variable keeps track of the number of letters printed so far.
        for key in self.keyboard_colors.keys():
            if i == 10:  # If i equals 10 or 19, print whitespaces and newlines for spacing.
                print("\n  ", end="")
            elif i == 19:
                print("\n     ", end="")
            print(f"[{color_text(key, self.keyboard_colors[key])}]", end="")  # Print the current letter in key, and color it based off its value in keyboard_colors.
            i += 1
        print("")  # Print a final newline character for spacing.

    '''
    Check Input Logic
    Check user input by first looping over the guess once checking for any characters in the
    correct position. If something is in the correct position, set its color to green (3), and decrease
    the frequency by 1. Loop through the guess a second time looking for characters in the wrong
    position. Only mark it as yellow (2) if it isn't already green, the letter is actually in the answer, and
    there is still remaining uses of this letter in letter_frequency. Lastly, if a letter is unused
    set its keyboard color to grey if and only if the keyboard color hasn't already been set to green or yellow.
    Returns 2 if the word was guessed.
    Returns 1 if all guesses were used.
    Returns 0 if word wasn't guessed and there are guesses remaining.
    '''
    def check_input(self, guess):
        letter_frequency = self.reset_letter_frequency()  # Reset the frequency of each letter to check this guess.
        guess_colors = [1, 1, 1, 1, 1]                    # Set all characters incorrect to start.

        # Check to see if any letters of the guess are in the correct spot
        for i, letter in enumerate(guess):
            if letter == self.answer[i]:         # If the letter is correct; Set colors to green, decrease frequency
                guess_colors[i] = 3
                self.keyboard_colors[letter] = 3
                letter_frequency[letter] -= 1

        # Loop through the guess a second time to check for yellow and grey letters.
        for i, letter in enumerate(guess):
            if guess_colors[i] != 3 and letter in self.answer and letter_frequency[letter] != 0:  # Mark yellow if not green, it's in the answer, and still has remaining uses.
                guess_colors[i] = 2
                if self.keyboard_colors[letter] != 3:  # Only set keyboard to yellow if not already green.
                    self.keyboard_colors[letter] = 2
                letter_frequency[letter] -= 1
            elif self.keyboard_colors[letter] == 0:  # Otherwise, only change color of on-screen keyboard to grey if it isn't green or yellow.
                self.keyboard_colors[letter] = 1

        # Lastly loop through the guess one final time in order to update the on-screen board.
        for i, letter in enumerate(guess):
            self.board[self.current_row][i] = color_text(letter, guess_colors[i])

        victory = all(letter == 3 for letter in guess_colors)  # Game is won if all guess colors are green.
        self.current_row += 1  # Increment to next row

        if victory:                  # If player won, return 2.
            return 2
        elif self.current_row >= 6:  # If there are no rows remaining return 1.
            return 1
        else:                        # Otherwise return 0.
            return 0


def main():
    print(colored(255, 255, 255, ""), end="")  # sets all text to white (unless specified with color_text function)
    board = Game()
    board.print_board()
    win_condition = 0
    while win_condition == 0:
        guess = input("Input Guess: ").strip().upper()
        while guess not in valid_inputs:
            guess = input("Input Guess: ").strip().upper()
        win_condition = board.check_input(guess)
        board.print_board()
    if win_condition == 2:
        print("--Congrats you won!--")
    elif win_condition == 1:
        print(f"--Nice try, the word was {board.answer}!--")


if __name__ == "__main__":
    main()
