# run export LC_ALL=C to avoid locale errors
import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
import random
import logging
import string
import colorama
from colorama import Fore, Back, Style
import time

colorama.init(autoreset=True)

logging.basicConfig(level=logging.DEBUG)
# vars
insults = [
    "My gran could do better! And she’s dead!", 
    "Don't just stand there like a big f—ing muffin!", 
    "Oops, my bad. I could’ve sworn I was dealing with an adult.",
    "Someday you’ll go far. And I really hope you stay there.",
    "I was today years old when I realized I didn’t like you.",
    " Your face makes onions cry.",
    "Keep rolling your eyes, you might eventually find a brain.",
    ]
pre_words_dict = {
    'app': "A software package",
    'xbox': "Microsoft's console brand"
}
pre_words_list = list(pre_words_dict.items())

system_word_choice  = random.choice(pre_words_list) # list of the words dict item
logging.debug(f"\nWORD: {system_word_choice[0]} MEANING: {system_word_choice[1]}")

hidden_word_list = ["_" for char in system_word_choice[0]]
# logging.debug(f"{hidden_word}")
# for letter in range(len(system_word_choice[0])):
#     hidden_word_list.append("_")
hidden_word = ("".join([items for items in hidden_word_list]))
logging.debug(f"{Fore.GREEN}HIDDEN WORD: {hidden_word}")


incorrect_guesses = 0
incorrect_guesses_limit = 20
# functions
def getKeyPress(e):
    global incorrect_guesses
    keypress = str(e.char).lower()
    if keypress not in string.ascii_letters:
        print(keypress)
    else:
        if keypress in system_word_choice[0]:
            if keypress in hidden_word_list:
                 pass
            else:
                print(f"{Fore.CYAN}That's a right guess")
                resetVar(keypress)
                isCorrect(True, keypress)
        else:
            incorrect_guesses +=1
            incorrect_guesses_var.set(f"Incorrect Guesses: {incorrect_guesses}")
            print(f"{Fore.RED}Incorrect Guess")
            isCorrect(False, keypress)
            if incorrect_guesses == incorrect_guesses_limit:
                print(f"{Fore.LIGHTYELLOW_EX}Limit Reached")
                result = messagebox.askretrycancel(f"Do you want to play again?", f"{random.choice(insults)}")
                if result:
                    restart_game()
                else:
                    window.quit()
                pass


def resetVar(letter):
    global hidden_word, hidden_word_list, correct_guesses
    # logging.debug(f"{letter}")
    for i in range(len(hidden_word_list)):
        if system_word_choice[0][i] == letter:
                hidden_word_list[i] = letter
                correct_guesses += 1
                score_label_var.set(f"Correct Guesses: {correct_guesses}")

    hidden_word = ["".join([items for items in hidden_word_list])]
    # logging.warning(f"{hidden_word_list}")
    word_label_var.set(hidden_word)
    checkState()

def isCorrect(correct: bool, last_guess: str):
    if correct:
        was_correct_var.set(f"Last guess '{last_guess}': Correct!")
        pass

    else:
        was_correct_var.set(f"Last guess '{last_guess}':Wrong!")
    pass
    
def checkState():
    if correct_guesses == len(system_word_choice[0]):
        print(f"{Fore.GREEN}Game won")
        result = messagebox.askretrycancel("Do you want to try again", "You won!,\nNot bad, next time :)")
        if result:
            restart_game()
        else:
            window.quit()

def restart_game():
    global system_word_choice, hidden_word_list, hidden_word, correct_guesses, incorrect_guesses

    # Reset game variables to their initial values
    system_word_choice  = random.choice(pre_words_list)
    hidden_word_list = ["_" for char in system_word_choice[0]]
    hidden_word = ("".join([items for items in hidden_word_list]))
    correct_guesses = 0
    incorrect_guesses = 0

    # Update the UI with the new values
    word_label_var.set(hidden_word)
    score_label_var.set(f"Correct Guesses: {correct_guesses}")
    incorrect_guesses_var.set(f"Incorrect Guesses: {incorrect_guesses}")
    hint_label.config(text=f"HINT: {system_word_choice[1]}")
    

# Setup
window = ttk.Window(themename='cyborg')
window.title('app')
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window.geometry('600x250')

# widgets
# Widget variables
word_label_var = tk.StringVar(value=hidden_word)
correct_guesses = 0
score_label_var = tk.StringVar(value=f"Correct Guesses: {correct_guesses}")
incorrect_guesses_var = tk.StringVar(value=f"Incorrect Guesses: {incorrect_guesses}")
was_correct_var = tk.StringVar(value=f"Last guess: ")

word_label = ttk.Label(window, text='', textvariable=word_label_var, font=('Calibri', 30))
word_label.pack(pady=5)

hint_label = ttk.Label(window, text=f"HINT: {system_word_choice[1]}", font=('Calibri', 12))
hint_label.pack(pady=10)

score_label = ttk.Label(window, textvariable=score_label_var, font=('Calibri', 18))
score_label.pack(pady=20)

incorrect_guesses_label = ttk.Label(window, textvariable=incorrect_guesses_var)
incorrect_guesses_label.pack()

was_correct = ttk.Label(window, text=f"", textvariable=was_correct_var)
was_correct.pack()


# Security event
window.bind('<Escape>', lambda event: window.quit())
window.bind('<KeyPress>', lambda event: getKeyPress(event))
# Run
window.mainloop()