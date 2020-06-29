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
                                           width=50, bg='pink',
                                           text='Hangman Game',
                                           font='Arial 16 bold',pady=10,
                                           padx=10)
                self.heading_label.grid(row=0)

                self.instructions_label = Label(self.main_frame,
                                                bg='red', width=70,
                                                wrap=600, text=
'''Welcome to Hangman. If you would like to import a custom set of phrases or words, press the 'Import Wordlist' button. The game will use the default list automatically. If you would like to see your game statistics for this session press the 'Game History' button, you can also export your statistics to a text file from that window if you would like. Press the 'Random Word' button to start a game using a word from the current wordlist. Press the 'Chosen Word' to create a game using a word you have entered.''',
                                                font='Arial 12', justify=LEFT,
                                                pady=10, padx=10)
                self.instructions_label.grid(row=1)


                # Buttons frame (row 2)
                self.buttons_frame = Frame(self.main_frame, pady=10, bg='green')
                self.buttons_frame.grid(row=3)


                # Buttons (In order)
                # Import Wordlist     (row 0, column 0)
                # Game History        (row 0, column 1)
                # Random phrase       (row 0, column 2)
                # Chosesn phrase      (row 0, column 3)
                self.wordlist_button = Button(self.buttons_frame, pady=10,
                                            padx=10, bg='white',
                                            text='Import Wordlist',
                                            font='Arial 10', command= lambda:
                                            self.wordlist_window(self.wordlist))
                self.wordlist_button.grid(row=0,column=0,padx=25)

                self.history_button = Button(self.buttons_frame, pady=10,
                                             padx=10, bg='white',
                                             text='Game History',
                                             font='Arial 10', command=
                                             self.history_window)
                self.history_button.grid(row=0,column=1,padx=25)

                self.random_button = Button(self.buttons_frame, pady=10,
                                            padx=10, bg='white',
                                            text='Random Word',
                                            font='Arial 10', command=
                                            self.game_information)
                self.random_button.grid(row=0,column=2,padx=25)

                self.chosen_button = Button(self.buttons_frame, pady=10,
                                            padx=10, bg='white',
                                            text='Chosen Word',
                                            font='Arial 10', command=
                                            self.game_information)
                self.chosen_button.grid(row=0,column=3,padx=25)

        def wordlist_window(self,wordlist):
                WordlistWindow(self,wordlist)

        def history_window(self):
                HistoryWindow(self)

        def game_information(self):

                # If the user has not selected a wordlist prompt them to do so
                if not self.wordlist:
                        WordlistWindow(self,self.wordlist)

        def game_window(self):
                GameWindow(self)

        #def get_wordlist(self)

class WordlistWindow:
        def __init__(self,partner,wordlist):

                # Running import def
                self.import_wordlists()

                # Creating window
                self.wordlist_box = Toplevel()


                # Creating frame
                self.wordlist_frame = Frame(self.wordlist_box, width=1000,
                                            height=1000, bg='white',)
                self.wordlist_frame.grid()


                # Disabling wordlist window button on main window
                partner.wordlist_button.config(state=DISABLED)


                # Creating label for instructions (row=0)
                self.instructions_label = Label(self.wordlist_frame,
                                                font='Arial 10', text=
'''Use the buttons below to select the list of phrases for the game to use when selecting a word. If you would like to add more lists then add text files to the same folder as the program, formatted in the same way as the other lists.'''
                                        , justify=LEFT, wrap=500,
                                        padx=10,pady=10,)
                self.instructions_label.grid(row=0)


                # If there is no wordlist selected display this instead.
                if not wordlist:
                        self.instructions_label.configure(self.wordlist_frame,
                                                          font='Arial 10', text=
'''You have not yet selected a list of phrases for the game to use! Press the buttons below to select the list of phrases for the game to use when selecting a word. If you would like to add more lists then add text files to the same folder as the program, formatted in the same way as the other lists.''' )


                # Deleting the window when the X is pressed
                self.wordlist_box.protocol('WM_DELETE_WINDOW',partial
                                           (self.close_wordlist,partner))


                # GUI Frame for imported lists
                self.wordlist_import_frame = Frame(self.wordlist_frame, width=
                                                   800, height=800, pady=10)
                self.wordlist_import_frame.grid(row=0)

        def close_wordlist(self,partner):

                # Re-enabling wordlist button and closing window.
                partner.wordlist_button.config(state=NORMAL)
                self.wordlist_box.destroy()

        def import_wordlist(self,wordlists):

                # For each text file in the directory of the program read it.


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