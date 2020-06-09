# Hangman Game made in Tkinter
# Jack Briggs


# Importing librarys

from tkinter import *
from functools import partial
import random
import time

class MainWindow:
        def __init__(self,partner):

                # Setting variables
                self.wordlist = []
                self.phrase = ''
                self.letters = []
                self.guesses = 10


                # Creating the frame for the window
                self.main_frame = Frame(width=1024, height=728, bg='white',
                                        pady=10,padx=10)
                self.main_frame.grid()


                # Creating heading label      (row 0)
                # Creating instructions label (row 1)
                self.heading_label = Label(self.main_frame,
                                           width=800, height=20, bg='white',
                                           text='Hangman Game',
                                           font='Arial 24 bold',pady=10,
                                           padx=10)
                self.heading_label.grid(row=0)







if __name__ == "__main__":
        root = Tk()
        root.title("Hangman Game")
        something = MainWindow(root)
        root.mainloop()