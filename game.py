import re
import random
from os import system, name

# list of all possible answers for the game
with open('Answers.txt', 'r') as f:
    answers = list(f)

# list of all possible guesses and answers that make up valid inputs
with open('AnswersAndGuesses.txt', 'r') as f:
    valid_inputs = list(f)

pboard = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'A', 'S', 'D', 'F', 'G', 'H',
          'J', 'K', 'L', 'Z', 'X', 'C', 'V', 'B', 'N', 'M']

kboard = 'QWERTYUIOPASDFGHJKLZXCVBNM'
# kboard ^^ stays STATIC as a means to search the keyboard and find the index value to edit pboard
kcolors = {'Q': '0', 'W': '0', 'E': '0', 'R': '0', 'T': '0', 'Y': '0', 'U': '0', 'I': '0', 'O': '0',
           'P': '0', 'A': '0', 'S': '0', 'D': '0', 'F': '0', 'G': '0', 'H': '0', 'J': '0', 'K': '0',
           'L': '0', 'Z': '0', 'X': '0', 'C': '0', 'V': '0', 'B': '0', 'N': '0', 'M': '0'}
# kcolors ^^ dictionary that keeps track of the color values of all keys on the keyboard


def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux
    else:
        _ = system('clear')


def errorcheck(pattern, value):
    while not re.match(pattern, value):
        value = input("Please enter a correct value: ")
    return value


def colored(r, g, b, text):  # ascii escape sequence code for color
    return "\033[38;2;{};{};{}m{}\033[38;2;255;255;255m".format(r, g, b, text)


print(colored(255, 255, 255, ""), end="")  # sets all text to white (unless specified)


class game:
    # 1) boxes: creates spaces to place each letter
    def __init__(self):
        self.boxes = [["□", "□", "□", "□", "□"], ["□", "□", "□", "□", "□"], ["□", "□", "□", "□", "□"],
                      ["□", "□", "□", "□", "□"], ["□", "□", "□", "□", "□"], ["□", "□", "□", "□", "□"]]
        self.crow = 0  # stands for current-row
        self.cword = str(answers[random.randint(0, len(answers) - 1)]).upper()  # current-word
        self.colors = [0, 0, 0, 0, 0]  # 0 = white 1 = yellow 2 = green

    def row(self, num):
        print("--", end="")
        for j in range(len(self.boxes[num])):
            print(f" {self.boxes[num][int(j)]} ", end="")  # for loop prints 1 row of boxes based on num
        print("--")

    def printBoard(self):
        for r in range(len(self.boxes)):  # calls on row function, loops 6 times
            self.row(int(r))

    def checkInput(self, guessed):
        totl = {}  # total letters - dict for frequency of letters in cword
        yletter = [' ', ' ', ' ', ' ', ' ']  # stores all yellow letter in guess
        usedletters = []  # each letter can only have one entry
        for w in range(len(self.cword)):
            if not re.search(self.cword[w], str(usedletters)):
                usedletters.append(self.cword[w])
                totl[self.cword[w]] = 1
            elif totl[self.cword[w]] >= 1:  # if already IN dictionary, increment by 1
                totl[self.cword[w]] += 1
            else:  # failsafe if neither are met, set to 1
                totl[self.cword[w]] = 1
        self.colors = [0, 0, 0, 0, 0]  # resets color values
        for w in range(len(guessed)):
            replace = 1  # edit dict once per letter
            yreplace = 1  # one failsafe replace for letter
            for match in re.finditer(guessed[w], self.cword):
                if int(match.start()) == w and int(totl[str(guessed[w])]) > 0:  # if pos match AND dict remaining
                    self.colors[w] = 2
                    yletter[w] = ' '  # resets yellow letter in this pos
                elif int(match.start()) != w and int(totl[str(guessed[w])]) > 0:
                    if not self.colors[w] == 2:  # don't overwrite green color
                        self.colors[w] = 1
                        yletter[w] = str(guessed[w])
                if int(match.start()) == w and int(totl[str(guessed[w])]) <= 0:  # *FAILSAFE* if green match but dict =0
                    yletter = str("".join(yletter))  # change yletter to str
                    if re.search(guessed[w], yletter) and yreplace == 1:
                        removey = re.search(guessed[w], yletter).start()
                        for match2 in re.finditer(guessed[w], yletter):
                            removey = match2.start()  # finds position of yletter to remove
                        self.colors[removey] = 0
                        self.colors[w] = 2
                        yletter = list(yletter)  # convert yletter -> list
                        yletter[removey] = " "  # remove yletter
            if re.search(guessed[w], self.cword) and replace == 1:
                totl[str(guessed[w])] -= 1  # increment dict down by 1
                replace = 0

    @staticmethod
    def letterBank():  # print function for keyboard
        print("---Used Letters:---")
        for i in range(len(kboard)):
            if i == 10:
                print("")
                print("  ", end="")
            elif i == 19:
                print("")
                print("     ", end="")
            elif i == 25:
                print(f"[{pboard[i]}]")

            if i < 10:  # prints first row
                print(f"[{pboard[i]}]", end="")
            elif i < 19:  # prints second row
                print(f"[{pboard[i]}]", end="")
            elif i < 25:  # print third row
                print(f"[{pboard[i]}]", end="")

    def checkWinner(self):
        if str(self.colors) == "[2, 2, 2, 2, 2]":  # colors all green when guess == cword
            return True


again = True
while again:
    board = game()
    print("---Welcome to The Game!---")
    while not board.checkWinner() and board.crow <= 5:  # max rows 5 (index start at 0)
        board.printBoard()
        board.letterBank()
        guess = input("Guess a word: ").upper()
        while not re.match("^[A-Z]{5}$", guess) or not re.search(guess, str(valid_inputs).upper()):
            guess = input("Please enter a valid word: ").upper()
        board.checkInput(guess)
        for l in range(len(guess)):
            pos = re.search(guess[l], kboard).start()  # gets index for keyboard
            if board.colors[l] == 0:  # if the current color val of letter is 0, print as grey
                board.boxes[board.crow][l] = colored(180, 180, 180, guess[l])
                if kcolors[guess[l]] == '0':  # if key ISN'T yellow or green, set to dark grey
                    pboard[pos] = colored(100, 100, 100, guess[l])
                    kcolors[guess[l]] = '0'  # set key to grey
            elif board.colors[l] == 1:  # if the current color val of letter is 1, print as yellow
                board.boxes[board.crow][l] = colored(255, 255, 0, guess[l])
                if kcolors[guess[l]] == "0":  # if key ISN'T yellow or green, set to yellow
                    pboard[pos] = colored(255, 255, 0, guess[l])
                    kcolors[guess[l]] = "1"  # set key to yellow
            elif board.colors[l] == 2:  # if the current color val of letter is 2, print as green
                board.boxes[board.crow][l] = colored(0, 255, 0, guess[l])
                pboard[pos] = colored(0, 255, 0, guess[l])
                kcolors[guess[l]] = "2"  # green can override all colors as it is the most prominent
        board.crow += 1  # increment to next row
        clear()

    clear()
    board.printBoard()
    board.letterBank()
    if board.checkWinner():
        print("------You guessed the word!------")
    else:
        print(f"-----The word was: {board.cword}, nice try!-----")
    selection = str(input("Do you want to play again? (1) Yes (2) No :"))
    selection = errorcheck('^([12])$', selection)
    if selection == "2":
        again = False
    elif selection == "1":
        clear()
        pboard = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'A', 'S', 'D', 'F', 'G', 'H',
                  'J', 'K', 'L', 'Z', 'X', 'C', 'V', 'B', 'N', 'M']
        kboard = 'QWERTYUIOPASDFGHJKLZXCVBNM'
        kcolors = {'Q': '0', 'W': '0', 'E': '0', 'R': '0', 'T': '0', 'Y': '0', 'U': '0', 'I': '0', 'O': '0',
                   'P': '0', 'A': '0', 'S': '0', 'D': '0', 'F': '0', 'G': '0', 'H': '0', 'J': '0', 'K': '0',
                   'L': '0', 'Z': '0', 'X': '0', 'C': '0', 'V': '0', 'B': '0', 'N': '0', 'M': '0'}  # reset values
