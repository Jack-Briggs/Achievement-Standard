# Hangman Game made in Tkinter
# Jack Briggs


# Importing librarys

from tkinter import *
from functools import partial
from random import randint
from PIL import Image, ImageTk
#import time
#import numpy
import glob
import os

class MainWindow:
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
                                           font='Candara 16 bold',pady=10,
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
                                             self.gamestats_window)
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

        def gamestats_window(self):

                # Check if there are any statistics, if no games have been
                # played tell the user and don't open the window.

                if len(InfoDump().get_games()) >0:
                        GameStatistics(self)

                else:
                        self.instructions_label.configure(text='You have not played any games!\nThere are no statistics avaliable.')

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

                # If the user has not selected a wordlist prompt them to do so
                if not InfoDump.wordlist:
                        WordlistWindow(self)
                else:
                        # Pick a random word from the wordlist to use for the game
                        InfoDump.word = InfoDump().get_wordlist()
                        InfoDump.word = InfoDump.word[randint(0,len(InfoDump().get_wordlist())-1)]


                        # Get the letters and start the game
                        InfoDump.characters = [char for char in InfoDump.word.lower()]
                        self.game_window()

        def chosen_word(self):

                # Get the word from the entry and split it into characters
                InfoDump.word = self.word_entry.get()
                InfoDump.characters = [char for char in InfoDump.word.lower()]


                # If the entry is not alphabetical ask for another entry.
                if all(char in self.allowed_characters for char in InfoDump.word):

                        # Remove the window and start the game
                        self.entry_box.protocol('WM_DELETE_WINDOW')
                        self.entry_box.destroy()
                        self.game_window()

                else:

                        self.entry_label.configure(text='Enter a word',fg='red')



class WordlistWindow:

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
                                           str(InfoDump.wordlist_key), pady=10, bg='white')
                self.display_label.grid(row=1)


                # If there is no wordlist selected change instructions message.
                # Also change the 'selected wordlist' label to 'None' instead
                # of []
                if not InfoDump.wordlist:
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
                InfoDump.wordlist_key=keynames[n]
                self.select_wordlist()


        def select_wordlist(self):

                # Select the corresponding list from the key
                # Change the label to display the chosen list.
                if InfoDump.wordlist_key in self.lists_dict.keys():
                        InfoDump.wordlist = self.lists_dict[InfoDump.wordlist_key]
                        self.display_label.configure(text='Current Wordlist: '+str(InfoDump.wordlist_key))



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

class GameWindow:

        def __init__(self,partner):

                # Vars
                self.temp_guesses = 9
                self.temp_time = '30'
                self.guessed_letters = []
                self.word_letters = InfoDump().get_characters()
                self.guessed_word_letters = ['_' for i in InfoDump().get_word()]
                self.letter = ''
                self.letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m',
                           'n','o','p','q','r','s','t','u','v','w','x','y','z']

                # Game Box
                self.game_box = Toplevel()


                # Game Frame
                self.game_frame = Frame(self.game_box,width=800,height=800,
                                        bg='white')
                self.game_frame.grid()


                # Hangman picture (row 0)
                self.img = ImageTk.PhotoImage(Image.open("test.png"))
                self.game_image = Label(self.game_frame,image=self.img)
                self.game_image.grid(row=0)


                # Display label (Phrase the game is using) (row 1)
                self.word_label = Label(self.game_frame,font='Arial 20',text=
                                        self.guessed_word_letters)
                self.word_label.grid(row=1)


                # Info frame (row 2, column 0)
                self.info_frame = Frame(self.game_frame)
                self.info_frame.grid(row=2)


                # Guesses used label (row 0, column 0)
                self.guesses_label = Label(self.info_frame,font='Arial 10',text="Guesses remaining: "+
                                           str(self.temp_guesses+1))
                self.guesses_label.grid(row=0)


                # Time taken label (row 0, column 1)
                self.time_label = Label(self.info_frame,font='Arial 10',text=
                                        'Timer: '+self.temp_time)
                self.time_label.grid(row=0,column=1)


                # Alphabet buttons frame (row 3)
                self.alphabet_frame = Frame(self.game_frame)
                self.alphabet_frame.grid(row=3)
                # For each letter add a button to the GUI
                # Get the keynames for each list
                rownum=0
                columnnum=0
                self.button_identities = []
                self.keynames = []
                for i in self.letters:
                        # creating the buttons, assigning a unique argument (i) to run the function (find_button)
                        button = Button(self.alphabet_frame, width=6, text=str([letter for letter in self.letters][self.letters.index(i)]), command=partial(self.run_checks, i))
                        button.grid(row=rownum,column=columnnum)
                        columnnum+=1
                        if columnnum >= 13:
                                columnnum = 0
                                rownum+=1
                        # add the button's identity to a list:
                        self.button_identities.append(button)


                # Guessed letters area (Game Frame, row 4)
                self.guessed_label = Label(self.game_frame,text='',font='Aral 10',pady=10)
                self.guessed_label.grid(row=4)


                # Disabling menu buttons
                partner.chosen_button.config(state=DISABLED)
                partner.random_button.config(state=DISABLED)


                # Deleting window when X is pressed
                self.game_box.protocol('WM_DELETE_WINDOW',partial(
                                        self.close_game,partner))


        def run_checks(self,n):

                # Defining some variables
                indices = []
                wrd_chars = InfoDump().get_characters()
                self.games = InfoDump().get_games()

                # Variables for game stats
                self.game_num = 0
                self.time_taken = 0
                self.guesses_used = 0
                self.win_loss = ''
                self.phrase = InfoDump().get_word()
                self.game_stats = []


                # Checks which button was pressed, stores the letter assigned,
                # disables the button and checks if the letter is in the word,
                # if the letter is in the word continue
                if bname := (self.button_identities[self.letters.index(n)]):
                        letter = n
                        bname.config(state=DISABLED)

                        # if correct guess don't subtract one
                        if letter in wrd_chars:
                                self.temp_guesses += 1

                        # Get the index positions of the letter in the word
                        for i in range(len(wrd_chars)):
                                if wrd_chars[i] == letter:
                                        indices.append(i)

                        # Replace the hidden letters on the display with
                        # correctly guessed letters
                        for p in indices:
                                self.guessed_word_letters[p] = letter
                                self.word_label.configure(text=self.guessed_word_letters)


                # Adding the guessed letter to a list
                # Updating the label
                self.guessed_letters.append(letter)
                self.guessed_label.configure(text=self.temp_guesses)

                # check if the player has won
                # if the player has guesses, lower the guesses by 1
                # update the image coresponding to the guess

                if '_' in self.guessed_word_letters:

                        # If the user has guesses subtract one
                        if self.temp_guesses >0:
                                self.temp_guesses -= 1
                                self.guesses_label.configure(text="Guesses remaining: "+str(self.temp_guesses+1))

                        # if the user has no more guesses end the game,
                        elif self.temp_guesses == 0:
                                self.temp_guesses = 0
                                self.guesses_label.configure(text="Guesses remaining: "+str(self.temp_guesses))

                                # disable the buttons on game end
                                for bname in self.button_identities:
                                        bname.config(state=DISABLED)

                                # If they lost
                                self.win_loss = 'Loss'

                else:
                        # Disable the buttons on game end
                        for bname in self.button_identities:
                                bname.config(state=DISABLED)

                        # if they win
                        self.win_loss = 'Win'

                print(self.temp_guesses)

                # Save the stats for this game
                self.game_num += 1
                self.time_taken = 0

                self.game_stats.append(str(self.game_num))
                self.game_stats.append(self.phrase)
                self.game_stats.append(self.win_loss)
                self.game_stats.append(str(self.time_taken))
                self.game_stats.append(str(self.temp_guesses))

                self.games.append(self.game_stats)

                # Send the games through to the main class
                InfoDump.games = self.games

        def close_game(self,partner):

                partner.chosen_button.config(state=NORMAL)
                partner.random_button.config(state=NORMAL)
                self.game_box.destroy()

class GameStatistics:

        def __init__(self,partner):


                # Get the games
                self.games = InfoDump().get_games()
                print(InfoDump().get_games())
                print(self.games)

                # Stats box
                self.stats_box = Toplevel()

                # Master Frame
                self.master_frame = Frame(self.stats_box)
                self.master_frame.grid()

                # Info Label
                self.info_label = Label(self.master_frame,font='Arial 12',text='This is the statistics screen, it will display the games for the session.\nClick the buttons to re-order your games based on that setting.')
                self.info_label.grid(row=1)

                #S Sorting Buttons Frame
                self.sorting_buttons_frame = Frame(self.master_frame)
                self.sorting_buttons_frame.grid(row=2)

                # Sorting Buttons
                self.phrase_button = Button(self.sorting_buttons_frame,font='Arial 12',text='Phrase',command=self.sort_word)
                self.phrase_button.grid(row=0, column=0)

                self.win_loss_button = Button(self.sorting_buttons_frame,font='Arial 12',text='Win / Loss',command=self.sort_winloss)
                self.win_loss_button.grid(row=0, column=1)

                self.time_button = Button(self.sorting_buttons_frame,font='Arial 12',text='Time Taken',command=self.sort_time)
                self.time_button.grid(row=0, column=2)

                self.guesses_button = Button(self.sorting_buttons_frame,font='Arial 12',text='Guesses Used',command=self.sort_guesses)
                self.guesses_button.grid(row=0, column=3)

                # Stats Frame
                self.statistics_frame = Frame(self.master_frame)
                self.statistics_frame.grid(row=3)

                # Displaying Games
                rownum = 0
                for game in self.games:
                        self.game_label = Label(self.statistics_frame,font='Arial 10',text=(sorted(self.games, key=lambda values: values[0])[rownum]))
                        self.game_label.grid(row=rownum)
                        rownum += 1

        def sort_word(self):
                self.game_label.destroy
                rownum = 0
                for game in self.games:
                        self.game_label = Label(self.statistics_frame,font='Arial 10',text=(sorted(self.games, key=lambda values: values[1])[rownum]))
                        self.game_label.grid(row=rownum)
                        rownum += 1

        def sort_winloss(self):
                self.game_label.destroy
                rownum = 0
                for game in self.games:
                        self.game_label = Label(self.statistics_frame,font='Arial 10',text=(sorted(self.games, key=lambda values: values[2],reverse=True)[rownum]))
                        self.game_label.grid(row=rownum)
                        rownum += 1

        def sort_time(self):
                self.game_label.destroy
                rownum = 0
                for game in self.games:
                        self.game_label = Label(self.statistics_frame,font='Arial 10',text=(sorted(self.games, key=lambda values: values[3])[rownum]))
                        self.game_label.grid(row=rownum)
                        rownum += 1

        def sort_guesses(self):
                self.game_label.destroy
                rownum = 0
                for game in self.games:
                        self.game_label = Label(self.statistics_frame,font='Arial 10',text=(sorted(self.games, key=lambda values: values[4])[rownum]))
                        self.game_label.grid(row=rownum)
                        rownum += 1

class InfoDump():

        word = ''
        characters = []
        games = []
        wordlist = []
        wordlist_key = ''

        def  __init__(self):
                print('Initialzing')

        def get_wordlist(self):
                return InfoDump.wordlist

        def get_wordlist_key(self):
                return InfoDump.wordlist_key

        def get_word(self):
                return InfoDump.word

        def get_games(self):
                return InfoDump.games

        def get_characters(self):
                return InfoDump.characters




if __name__ == "__main__":
        root = Tk()
        root.title("Hangman Game")
        something = MainWindow(root)
        root.mainloop()

