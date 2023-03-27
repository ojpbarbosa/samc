# this is the automation script for Stone Automata Maze Challenge phase 1
import keyboard
from time import sleep

# sequence = input().split(" ")
sequence = "d d r d r l r l d u d r d d u u u d d d l r r u r d u r u r r d d"

sleep(3)

for movement in sequence:
    if movement == "u":
        keyboard.press_and_release("up arrow")

    elif movement == "d":
        keyboard.press_and_release("down arrow")

    elif movement == "l":
        keyboard.press_and_release("left arrow")

    elif movement == "r":
        keyboard.press_and_release("right arrow")

    sleep(0.1)
