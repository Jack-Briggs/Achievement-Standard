# Hangman Game made in Tkinter
# Jack Briggs


# Importing librarys

from tkinter import *
from functools import partial
import random
import time
import numpy

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
                                           width=80, bg='pink',
                                           text='Hangman Game',
                                           font='Arial 16 bold',pady=10,
                                           padx=10)
                self.heading_label.grid(row=0)

                self.instructions_label = Label(self.main_frame, width=80,
                                                bg='red', text='<instructions>',
                                                font='Arial 12',
                                                pady=10, padx=10)
                self.instructions_label.grid(row=1)


                # Buttons frame (row 2)
                self.buttons_frame = Frame(self.main_frame, pady=10, padx=10,
                                           bg='green')
                self.buttons_frame.grid(row=3)


                # Buttons
                # Import Wordlist (row 1, collumn 0)
                # Random phrase (row 0, collumn 1)
                # Chosesn phrase (row 2, collumn 0)
                # Game History  (row 1, collumn 2)
                self.import_button = Button(self.buttons_frame,
                                            pady=10, padx=10, bg='white',
                                            text='Import Wordlist' ,
                                            font='Arial 10')

                #self.random_button
                #self.chosen_button
                #self.history_button








if __name__ == "__main__":
        root = Tk()
        root.title("Hangman Game")
        something = MainWindow(root)
        root.mainloop()