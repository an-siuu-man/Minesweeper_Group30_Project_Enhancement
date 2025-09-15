"""
    Program Name: main.py
    Authors: Kusuma Murthy, Sophia Jacob, Anna Lin, Nikka Voung, Nimra Syed
    Creation Date: 8/29/2025
    Last modified: 9/15/2025
    Purpose: To act as the main starting point to run the code.
    Inputs: N/A
    Outputs: Run the code from game.py
    Collaborators: N/A
    Sources: N/A
"""

from game import Game

if __name__ == "__main__":
    minesweeper = Game()
    minesweeper.play_game()
