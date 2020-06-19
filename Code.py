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


                # Buttons (In order)
                # Import Wordlist     (row 1, column 0)
                # Game History        (row 1, column 2)
                # Random phrase       (row 0, column 1)
                # Chosesn phrase      (row 2, column 0)
                self.import_button = Button(self.buttons_frame, pady=10,
                                            padx=10, bg='white',
                                            text='Import Wordlist',
                                            font='Arial 10', command=
                                            self.wordlist_window)
                self.import_button.grid(row=1,column=0)

                self.history_button = Button(self.buttons_frame, pady=10,
                                             padx=10, bg='white',
                                             text='Game History',
                                             font='Arial 10', command=
                                             self.history_window)
                self.history_button.grid(row=1,column=2)

                self.random_button = Button(self.buttons_frame, pady=10,
                                            padx=10, bg='white',
                                            text='Random Word',
                                            font='Arial 10', command=
                                            self.game_window)
                self.random_button.grid(row=0,column=1)

                self.chosen_button = Button(self.buttons_frame, pady=10,
                                            padx=10, bg='white',
                                            text='Chosen Word',
                                            font='Arial 10', command=
                                            self.game_window)
                self.chosen_button.grid(row=2,column=1)

        def wordlist_window(self):
                WordlistWindow(self)

        def history_window(self):
                HistoryWindow(self)

        #def game_information(self)

        def game_window(self):
                GameWindow(self)

        #def get_wordlist(self)

class WordlistWindow:
        def __init__(self,partner):

                # Temp window
                self.wordlist_box = Toplevel()
                self.wordlist_frame = Frame(self.wordlist_box,width=400,height=400,bg='white')
                self.wordlist_frame.grid()
                self.temp_label = Label(self.wordlist_frame,font='Arial 10',text='temp')
                self.temp_label.grid(row=0)
                partner.import_button.config(state=DISABLED)
                self.wordlist_box.protocol('WM_DELETE_WINDOW',partial(self.close_wordlist,partner))


        def close_wordlist(self,partner):

                partner.import_button.config(state=NORMAL)
                self.wordlist_box.destroy()

class HistoryWindow:
        def __init__(self,partner):

                # Temp window
                self.history_box = Toplevel()
                self.history_frame = Frame(self.history_box,width=400,height=400,bg='white')
                self.history_frame.grid()
                self.temp_label = Label(self.history_frame,font='Arial 10',text='temp')
                self.temp_label.grid(row=0)
                partner.history_button.config(state=DISABLED)
                self.history_box.protocol('WM_DELETE_WINDOW',partial(self.close_history,partner))


        def close_history(self,partner):

                partner.history_button.config(state=NORMAL)
                self.history_box.destroy()

class GameWindow:
        def __init__(self,partner):

                # Temp window
                self.game_box = Toplevel()
                self.game_frame = Frame(self.game_box,width=400,height=400,bg='white')
                self.game_frame.grid()
                self.temp_label = Label(self.game_frame,font='Arial 10',text='temp')
                self.temp_label.grid(row=0)
                partner.chosen_button.config(state=DISABLED)
                partner.random_button.config(state=DISABLED)
                self.game_box.protocol('WM_DELETE_WINDOW',partial(self.close_game,partner))


        def close_game(self,partner):

                partner.chosen_button.config(state=NORMAL)
                partner.random_button.config(state=NORMAL)
                self.game_box.destroy()

if __name__ == "__main__":
        root = Tk()
        root.title("Hangman Game")
        something = MainWindow(root)
        root.mainloop()