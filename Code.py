# Hangman Game made in Tkinter
# Jack Briggs



# Importing librarys

from tkinter import *
from functools import partial
from random import randint
from PIL import Image, ImageTk
import time
import glob
import os

class MainWindow:
        def __init__(self,partner):

                # Setting variables
                self.allowed_characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ '
                self.instructions_text = '''Welcome to Hangman. If you would like to import a custom set of phrases or words, press the 'Import Wordlist' button. The game will use the default list automatically. If you would like to see your game statistics for this session press the 'Game History' button, you can also export your statistics to a text file from that window if you would like. Press the 'Random Word' button to start a game using a word from the current wordlist. Press the 'Chosen Word' to create a game using a word you have entered.'''


                # Creating the frame for the window
                self.main_frame = Frame(width=1024, height=728, bg='grey',
                                        pady=10,padx=10)
                self.main_frame.grid()


                # Creating heading label      (row 0)
                # Creating instructions label (row 1)
                self.heading_label = Label(self.main_frame,
                                           width=50, bg='grey',
                                           text='Hangman Game',
                                           font='Candara 16 bold',pady=10,
                                           padx=10)
                self.heading_label.grid(row=0)

                self.instructions_label = Label(self.main_frame,
                                                bg='grey', width=70,
                                                wrap=600, text=
                                                self.instructions_text,
                                                font='Arial 12', justify=LEFT,
                                                pady=10, padx=10)
                self.instructions_label.grid(row=1)


                # Buttons frame (row 2)
                self.buttons_frame = Frame(self.main_frame, pady=10, bg='grey')
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
                        self.instructions_label.configure(text=self.instructions_text)

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
                # If the entry is blank or has too many characters ask again.
                if all(char in self.allowed_characters for char in InfoDump.word) and len(InfoDump.characters) <= 30 and len(InfoDump.characters) != 0:

                        # Remove the window and start the game
                        self.entry_box.protocol('WM_DELETE_WINDOW')
                        self.entry_box.destroy()
                        self.game_window()

                else:

                        self.entry_label.configure(text='Enter a word under 30 characters in length.',fg='red')



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
                                            height=1000, bg='grey',)
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
                                        padx=10,pady=10,bg='grey')
                self.instructions_label.grid(row=0)


                # Display the current wordlist for the program (row-1)
                self.display_label = Label(self.wordlist_frame, font='Arial 10',
                                           fg='red', text='Current Wordlist: '+
                                           str(InfoDump.wordlist_key), pady=10, bg='grey')
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
                                                   600, height=600, pady=10,bg='grey')
                self.wordlist_import_frame.grid(row=2)


                # For each wordlist add a button to the GUI
                # Get the keynames for each list
                rownum=0
                self.button_identities = []
                self.keynames = []
                for i in range(len(self.lists_dict.keys())):
                        # creating the buttons, assigning a unique argument (i) to run the function (find_button)
                        button = Button(self.wordlist_import_frame, width=60, text=str([key for key in self.lists_dict.keys()][i]), bg='grey',command=partial(self.find_button, i))
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
                self.timecheck = 0
                self.temp_guesses = 9
                self.time_taken = 0
                self.guessed_letters = []
                self.word_chars = [i for i in InfoDump().get_word().lower()]
                self.hidden_chars = []
                self.letter = ''
                self.letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m',
                           'n','o','p','q','r','s','t','u','v','w','x','y','z']
                self.serperator = ' '
                self.img_counter = 0

                # Logic to split the word into characters of
                # _ for letters and spaces for space
                for i in self.word_chars:
                        index = self.word_chars.index(i)

                        if self.word_chars[index] != ' ' :
                                self.hidden_chars.append('_')

                        elif self.word_chars[index] == ' ':
                                self.hidden_chars.append(' ')


                # Game Box
                self.game_box = Toplevel()


                # Game Frame
                self.game_frame = Frame(self.game_box,width=800,height=800,
                                        bg='grey')
                self.game_frame.grid()
                
                # Image Frame
                self.image_frame = Frame(self.game_frame,bg='grey')
                self.image_frame.grid(row=0,pady=100)


                # Hangman picture (row 0)
                self.game_image = Label(self.image_frame,bg='grey')
                self.game_image.grid(row=0)


                # Display label (Phrase the game is using) (row 2)
                self.word_label = Label(self.game_frame,font='Arial 20',text=
                                        self.serperator.join(self.hidden_chars),bg='grey')
                self.word_label.grid(row=2)


                # Info frame (row 3, column 0)
                self.info_frame = Frame(self.game_frame,bg='grey')
                self.info_frame.grid(row=3)


                # Guesses used label (row 0, column 0)
                self.guesses_label = Label(self.info_frame,font='Arial 10',text="Guesses remaining: "+
                                           str(self.temp_guesses+1),bg='grey')
                self.guesses_label.grid(row=0)


                # Time taken label (row 0, column 1)
                self.time_label = Label(self.info_frame,font='Arial 10',text=
                                        'Timer: '+str(self.time_taken),bg='grey')
                self.time_label.grid(row=0,column=1)


                # Win/Loss label (row 1)
                self.win_loss_label = Label(self.info_frame,font='Arial 24',text='',bg='grey')
                self.win_loss_label.grid(row=1)


                # Alphabet buttons frame (row 4)
                self.alphabet_frame = Frame(self.game_frame,bg='grey')
                self.alphabet_frame.grid(row=4)


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


                # Guessed letters area (Game Frame, row 5)
                self.guessed_label = Label(self.game_frame,text='',font='Aral 10',pady=10,bg='grey')
                self.guessed_label.grid(row=5)


                # Disabling menu buttons
                partner.chosen_button.config(state=DISABLED)
                partner.random_button.config(state=DISABLED)


                # Deleting window when X is pressed
                self.game_box.protocol('WM_DELETE_WINDOW',partial(
                                        self.close_game,partner))


                # Run the timer function and start the timer
                self.start = time.time()
                self.update_clock()

        def update_clock(self):

                # Count up 1 second
                self.end = time.time()
                self.time_taken = int(self.end-self.start)
                self.temptime = self.time_taken


                # Keep running the clock if the game is still going
                if self.timecheck != 1:
                        self.game_box.after(1000, self.update_clock)

                else:
                        self.time_taken -= 1


                # Update the label
                self.time_label.configure(text='Timer: '+str(self.time_taken))

        def run_checks(self,n):

                # Defining some variables
                indices = []
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
                        if letter in self.word_chars:
                                self.temp_guesses += 1
                                
                                # Get the index positions of the letter in the word
                                for i in range(len(self.word_chars)):
                                        if self.word_chars[i] == letter:
                                                indices.append(i)
        
                                # Replace the hidden letters on the display with
                                # correctly guessed letters
                                for p in indices:
                                        self.hidden_chars[p] = letter
                                        self.word_label.configure(text=self.serperator.join(self.hidden_chars))                                
                        
                        else:
                                self.img_counter = self.img_counter + 1


                # Pure garbage.
                # Checking which image to update to and then updating to it.
                if self.img_counter == 1:
                        self.img = ImageTk.PhotoImage(Image.open("1.png"))
                        self.game_image.configure(image=self.img)                
                elif self.img_counter == 2:
                        self.img = ImageTk.PhotoImage(Image.open("2.png"))
                        self.game_image.configure(image=self.img)
                elif self.img_counter == 3:
                        self.img = ImageTk.PhotoImage(Image.open("3.png"))
                        self.game_image.configure(image=self.img)
                elif self.img_counter == 4:
                        self.img = ImageTk.PhotoImage(Image.open("4.png"))
                        self.game_image.configure(image=self.img)
                elif self.img_counter == 5:
                        self.img = ImageTk.PhotoImage(Image.open("5.png"))
                        self.game_image.configure(image=self.img)
                elif self.img_counter == 6:
                        self.img = ImageTk.PhotoImage(Image.open("6.png"))
                        self.game_image.configure(image=self.img)
                elif self.img_counter == 7:
                        self.img = ImageTk.PhotoImage(Image.open("7.png"))
                        self.game_image.configure(image=self.img)
                elif self.img_counter == 8:
                        self.img = ImageTk.PhotoImage(Image.open("8.png"))
                        self.game_image.configure(image=self.img)
                elif self.img_counter == 9:
                        self.img = ImageTk.PhotoImage(Image.open("9.png"))
                        self.game_image.configure(image=self.img)
                elif self.img_counter == 10:
                        self.img = ImageTk.PhotoImage(Image.open("10.png"))
                        self.game_image.configure(image=self.img)                                
                                        


                # Adding the guessed letter to a list
                # Updating the label
                self.guessed_letters.append(letter)
                self.guessed_label.configure(text=self.guessed_letters)

                # check if the player has won
                # if the player has guesses, lower the guesses by 1
                # update the image coresponding to the guess

                if '_' in self.hidden_chars:

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
                                self.win_loss_label.configure(text='Game Over')
                                self.word_label.configure(text=self.word_chars)
                                self.timecheck = 1
                                self.history_calcs()

                else:
                        # Disable the buttons on game end
                        for bname in self.button_identities:
                                bname.config(state=DISABLED)

                        # if they win
                        self.win_loss = 'Win'
                        self.win_loss_label.configure(text='You won!')
                        self.timecheck = 1
                        self.history_calcs()

        def history_calcs(self):

                # Save the stats for this game
                self.game_num = InfoDump.gamenum
                self.game_num += 1

                self.game_stats.append(str(self.game_num))
                self.game_stats.append(str(self.phrase))
                self.game_stats.append(self.win_loss)
                self.game_stats.append(str(self.temptime))
                self.game_stats.append(str(self.temp_guesses))

                self.games.append(self.game_stats)

                # Send the games through to the main class
                InfoDump.games = self.games
                InfoDump.gamenum = self.game_num

        def close_game(self,partner):

                partner.chosen_button.config(state=NORMAL)
                partner.random_button.config(state=NORMAL)

                self.game_box.destroy()


class GameStatistics:

        def __init__(self,partner):


                # Get the games
                self.games = InfoDump().get_games()


                # Stats box
                self.stats_box = Toplevel()


                # Master Frame
                self.master_frame = Frame(self.stats_box)
                self.master_frame.grid()


                # Info Label
                self.info_label = Label(self.master_frame,font='Arial 12',text='This is the statistics screen, it will display the games for the session.\nClick the buttons to re-order your games based on that setting.')
                self.info_label.grid(row=1, pady=10)


                #S Sorting Buttons Frame
                self.sorting_buttons_frame = Frame(self.master_frame)
                self.sorting_buttons_frame.grid(row=2)


                # Sorting Buttons
                self.phrase_button = Button(self.sorting_buttons_frame,font='Arial 12',text='Phrase',command=self.sort_word)
                self.phrase_button.grid(row=0, column=0, padx=15)

                self.win_loss_button = Button(self.sorting_buttons_frame,font='Arial 12',text='Win / Loss',command=self.sort_winloss)
                self.win_loss_button.grid(row=0, column=1, padx=15)

                self.time_button = Button(self.sorting_buttons_frame,font='Arial 12',text='Time Taken',command=self.sort_time)
                self.time_button.grid(row=0, column=2, padx=15)

                self.guesses_button = Button(self.sorting_buttons_frame,font='Arial 12',text='Guesses Used',command=self.sort_guesses)
                self.guesses_button.grid(row=0, column=3, padx=15)


                # Stats Frame
                self.statistics_frame = Frame(self.master_frame)
                self.statistics_frame.grid(row=3)


                # Displaying Games
                rownum = 0
                for game in self.games:
                        self.game_label = Label(self.statistics_frame,font='Arial 10',text=(sorted(self.games, key=lambda values: values[0])[rownum]))
                        self.game_label.grid(row=rownum,pady=2)
                        rownum += 1


                # Export Button Frame
                self.export_frame = Frame(self.master_frame)
                self.export_frame.grid(row=4)


                # Export Button
                self.export_button = Button(self.export_frame,font='Arial 10',text='Export Stats',command=self.export_stats)
                self.export_button.grid(row=0)

                # Function to sort by the word the game was using
        def sort_word(self):
                self.game_label.destroy
                rownum = 0
                for game in self.games:
                        self.game_label = Label(self.statistics_frame,font='Arial 10',text=(sorted(self.games, key=lambda values: values[1])[rownum]))
                        self.game_label.grid(row=rownum)
                        rownum += 1

                # Function to sort by if the player won or lost
        def sort_winloss(self):
                self.game_label.destroy
                rownum = 0
                for game in self.games:
                        self.game_label = Label(self.statistics_frame,font='Arial 10',text=(sorted(self.games, key=lambda values: values[2],reverse=True)[rownum]))
                        self.game_label.grid(row=rownum)
                        rownum += 1
                        
                # Function to sort by how long the player took
        def sort_time(self):
                self.game_label.destroy
                rownum = 0
                for game in self.games:
                        self.game_label = Label(self.statistics_frame,font='Arial 10',text=(sorted(self.games, key=lambda values: values[3])[rownum]))
                        self.game_label.grid(row=rownum)
                        rownum += 1
                        
                # Function to sort by the amount of guesses used
        def sort_guesses(self):
                self.game_label.destroy
                rownum = 0
                for game in self.games:
                        self.game_label = Label(self.statistics_frame,font='Arial 10',text=(sorted(self.games, key=lambda values: values[4])[rownum]))
                        self.game_label.grid(row=rownum)
                        rownum += 1

        def export_stats(self):
                
                # Create a CSV file then write to it each game in the list
                with open('Gamestats.csv','w+') as file:
                        file.write('Game Number, ')
                        file.write('Phrase, ')
                        file.write('Win/Loss, ')
                        file.write('Time, ')
                        file.write('Guesses Used')
                        file.write('\n')
                        for i in self.games:
                                file.write(str(i))
                                file.write('\n')

class InfoDump():

        gamenum = 0
        word = ''
        characters = []
        games = []
        wordlist = []
        wordlist_key = ''

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