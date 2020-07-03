# Hangman Game made in Tkinter
# Jack Briggs


# Importing librarys

from tkinter import *
from functools import partial
from random import randint
#import time
#import numpy
import glob
import os

class MainWindow:

        word = ''
        characters = []

        def __init__(self,partner):

                # Setting variables
                self.allowed_characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ '


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
                                            text='Select Wordlist',
                                            font='Arial 10', command=
                                            self.wordlist_window)
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
                                            self.random_word)
                self.random_button.grid(row=0,column=2,padx=25)

                self.chosen_button = Button(self.buttons_frame, pady=10,
                                            padx=10, bg='white',
                                            text='Chosen Word',
                                            font='Arial 10', command=
                                            self.chosen_word_window)
                self.chosen_button.grid(row=0,column=3,padx=25)

        def wordlist_window(self):
                WordlistWindow(self)

        def history_window(self):
                HistoryWindow(self)

        def game_window(self):
                GameWindow(self)

        def chosen_word_window(self):

                # Create entry box
                self.entry_box = Toplevel()


                # Entry Frame
                self.entry_frame = Frame(self.entry_box,width=40,height=40)
                self.entry_frame.grid()


                # Entry Label
                self.entry_label = Label(self.entry_frame,text='Enter a Word',
                                         font='Arial 12',padx=20,pady=20)
                self.entry_label.grid(row=0)


                # Entry sub-frame
                self.entry_sub_frame = Frame(self.entry_frame,
                                             width=20,height=40)
                self.entry_sub_frame.grid(row=1)


                # Entry window
                self.word_entry = Entry(self.entry_sub_frame,text='Enter a Word'
                                        ,font='Arial 12')
                self.word_entry.grid(row=0,pady=10,padx=5)


                # Confirm button
                self.confirm_button = Button(self.entry_sub_frame,text='Confirm'
                                             ,font='Arial 12',
                                             command=self.chosen_word)
                self.confirm_button.grid(row=1,pady=10)

        def random_word(self):

                print(self.get_wordlist())

                # If the user has not selected a wordlist prompt them to do so
                if not WordlistWindow.wordlist:
                        WordlistWindow(self)
                else:
                        # Pick a random word from the wordlist to use for the game
                        self.word = self.get_wordlist()
                        self.word = self.word[randint(0,len(self.get_wordlist())-1)]


                        # Get the letters and start the game
                        self.characters = [char for char in self.word]
                        self.game_window()

        def chosen_word(self):

                # Get the word from the entry and split it into characters
                MainWindow.word = self.word_entry.get()
                MainWindow.characters = [char for char in self.word]


                # If the entry is not alphabetical ask for another entry.
                if all(char in self.allowed_characters for char in MainWindow.word):

                        # Remove the window and start the game
                        self.entry_box.protocol('WM_DELETE_WINDOW')
                        self.entry_box.destroy()
                        self.game_window()

                else:

                        self.entry_label.configure(text='Enter a word',fg='red')

        def get_wordlist(self):
                return WordlistWindow.wordlist

        def get_wordlist_key(self):
                return WordlistWindow.wordlist_key

        def get_word(self):
                return MainWindow.word

        def get_characters(self):
                return MainWindow.characters



class WordlistWindow:

        wordlist = []
        wordlist_key = ''

        def __init__(self,partner):

                # Definging variables and gathering the directory of the program
                self.file_path = os.path.dirname(os.path.realpath(__file__))
                self.lists_dict = {}


                # Running import definition
                self.import_wordlists(self.file_path)


                # Creating window
                self.wordlist_box = Toplevel()


                # Creating frame
                self.wordlist_frame = Frame(self.wordlist_box, width=1000,
                                            height=1000, bg='white',)
                self.wordlist_frame.grid()


                # Disabling wordlist window button on main window
                partner.wordlist_button.config(state=DISABLED)
                partner.random_button.config(state=DISABLED)
                partner.chosen_button.config(state=DISABLED)


                # Creating label for instructions (row=0)
                self.instructions_label = Label(self.wordlist_frame,
                                                font='Arial 10', text=
'''Use the buttons below to select the list of phrases for the game to use when selecting a word. If you would like to add more lists then add text files to the same folder as the program, formatted in the same way as the other lists.'''
                                        , justify=LEFT, wrap=500,
                                        padx=10,pady=10,)
                self.instructions_label.grid(row=0)


                # Display the current wordlist for the program (row-1)
                self.display_label = Label(self.wordlist_frame, font='Arial 10',
                                           fg='red', text='Current Wordlist: '+
                                           str(WordlistWindow.wordlist_key), pady=10, bg='white')
                self.display_label.grid(row=1)


                # If there is no wordlist selected change instructions message.
                # Also change the 'selected wordlist' label to 'None' instead
                # of []
                if not WordlistWindow.wordlist:
                        self.instructions_label.configure(text=
'''You have not yet selected a list of phrases for the game to use! Press the buttons below to select the list of phrases for the game to use when selecting a word. If you would like to add more lists then add text files to the same folder as the program, formatted in the same way as the other lists.''' )
                        self.display_label.configure(text=
'''Current Wordlist: None''')


                # Deleting the window when the X is pressed
                self.wordlist_box.protocol('WM_DELETE_WINDOW',partial
                                           (self.close_wordlist,partner))


                # GUI Frame for imported lists (row=2)
                self.wordlist_import_frame = Frame(self.wordlist_frame, width=
                                                   600, height=600, pady=10)
                self.wordlist_import_frame.grid(row=2)


                # For each wordlist add a button to the GUI
                # Get the keynames for each list
                rownum=0
                self.button_identities = []
                self.keynames = []
                for i in range(len(self.lists_dict.keys())):
                        # creating the buttons, assigning a unique argument (i) to run the function (find_button)
                        button = Button(self.wordlist_import_frame, width=60, text=str([key for key in self.lists_dict.keys()][i]), command=partial(self.find_button, i))
                        rownum+=1
                        button.grid(row=rownum)
                        # add the button's identity to a list:
                        self.button_identities.append(button)


        def find_button(self,n):

                # Function to get the index and identity of each button (bname)
                # So that I can figure out which one was pressed.
                # Get the names of each wordlist
                keynames = []
                for key in self.lists_dict.keys():
                        keynames.append(key)


                # Checks which button was pressed and disabled it
                # Enables all other buttons
                if bname := (self.button_identities[n]):
                        bname.config(state=DISABLED)
                        for bname in self.button_identities:
                                if bname in self.button_identities and bname != (self.button_identities[n]):
                                        bname.config(state=NORMAL)


                # Saving the wordlist name that corresponded to the button
                # that was pressed.
                # Running selecting function.
                WordlistWindow.wordlist_key=keynames[n]
                self.select_wordlist()


        def select_wordlist(self):

                # Select the corresponding list from the key
                # Change the label to display the chosen list.
                if WordlistWindow.wordlist_key in self.lists_dict.keys():
                        WordlistWindow.wordlist = self.lists_dict[WordlistWindow.wordlist_key]
                        self.display_label.configure(text='Current Wordlist: '+str(WordlistWindow.wordlist_key))



        def close_wordlist(self,partner):

                # Re-enabling wordlist button and closing window.
                partner.wordlist_button.config(state=NORMAL)
                partner.chosen_button.config(state=NORMAL)
                partner.random_button.config(state=NORMAL)
                self.wordlist_box.destroy()

        def import_wordlists(self,file_path):

                # For each text file in the directory of the program read it.
                # Making the program only use text files in the file path.
                file_path = str(self.file_path)+"/*.txt"
                for filename in glob.glob(file_path):
                        with open(filename) as f:

                                # Create a dictionary with the first row as key,
                                # then a list of the remaining lines as values.
                                # Update this dictionary for each file.
                                temp_list = []
                                rows = [row for row in f]
                                header = rows[0]
                                header = header.strip()
                                rows = rows[1:]
                                self.lists_dict[header] = ''
                                for i in rows:
                                        temp_list.append(i.strip())
                                self.lists_dict[header] = temp_list

                # Returns the dict when called
                return self.lists_dict

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

