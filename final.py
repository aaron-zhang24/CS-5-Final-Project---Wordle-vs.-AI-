import random
import copy
import colorama
from colorama import Fore

with open("sgb-words.txt", "r") as f:
    word_list = []
    for line in f.readlines():
        word_list += [line.strip()]

global_gameword = ''
ai_guess_count = 0
class Board():
    def __init__(self, width, height):
        '''Construct objects of type Board, with the given width and height.'''
        self.width = width
        self.height = height
        self.data = [[' ']* width for row in range(height)]
        self.game_word = random.choice(word_list)
        self.ai_guess_count = ai_guess_count
        self.user_words = []

    def __repr__(self):
        '''his method returns a string representation
           for an object of type Board for the player.'''
        s = '' # The string to return
        N = len(self.user_words)  
        for row in range(0, N):
            current_word = self.user_words[row]
            colored_user_guess = self.colorizor(current_word)
            s += colored_user_guess
            s += '\n'
        for row in range(N, self.height):
            s += '|'
            for col in range(0, self.width):
                s += self.data[row][col] + '|'
            s += '\n'

        s += (2*self.width + 1) * '-' + "\n"   # Bottom of the board
        # Add code here to put the numbers underneath
        for col in range(0, self.width):
            s+= " " + str(col) 
        return (Fore.WHITE + s)       # The board is complete; return it
    
    def addMove(self, word):
        '''Adds a word to the board.'''
        assert len(word) == self.width
        for row in range(self.height):
            if self.data[row][0] != ' ': # row has a word in it
                row += 1 # go down a row
            else:
                for i in range(len(word)):
                    self.data[row][i] = word[i]
                break

    def clear(self):
        '''Clear the game board of all game pieces.'''
        # loop through each tile
        for width in range(self.width):
            for height in range(self.height):
                if self.data[height][width] != ' ':
                    self.data[height][width] = ' '
    
    def feedback(self, ai_guess):
        '''Returns string with letters: 'w' (wrong), 'g'(correct), 'y' (correct but in wrong place) '''
        feedback_string = ''
        for i in range(len(ai_guess)):
            if ai_guess[i] == self.game_word[i]:
                feedback_string += 'g'
            elif ai_guess[i] in self.game_word: 
                feedback_string += 'y'
            else:
                feedback_string += 'w'
        return feedback_string
    
    def colorizor(self, user_guess):
        '''Returns colorized version of user_guess where green indicates correct letter and position,
        yellow indicates correct letter, wrong position, and red indicates incorrect letter.'''
        colored_user_guess = "|"
        user_guess_deepcopy = copy.deepcopy(user_guess)
        feedback_string = self.feedback(user_guess_deepcopy)
        for i in range(5):
            if feedback_string[i] == "g":
                colored_user_guess += (Fore.GREEN + user_guess[i])
            elif feedback_string[i] == "y":
                colored_user_guess += (Fore.YELLOW + user_guess[i])
            elif feedback_string[i] == "w":
                colored_user_guess += (Fore.RED + user_guess[i])
            colored_user_guess += (Fore.WHITE + '|')
        return colored_user_guess
  
    def ai_hard(self):
        '''Uses a 'good' strater word like arise as its first word and then proceeds.
        Returns: number of guesses it took for the AI to win if it was successful'''
        word_list_deepcopy = copy.deepcopy(word_list) # creates deep copy of word_list so it won't change the original word_list
        ai_guess = "arise" # chooses a random word from the word_list
        ai_guess_count = 0  # counter variable
        while ai_guess != self.game_word:
            tuple_words = tuple(word_list_deepcopy) 
            feedback_ai = self.feedback(ai_guess) # creates feedback list based on the ai's guess
            self.user_words += [ai_guess]
            self.addMove(ai_guess)
            ai_guess_count += 1
            for word in tuple_words: # modifies deep copy of word list so that the ai only chooses words that correspond with the feedback list
                for letters in range(5):
                    if feedback_ai[letters] == 'w' and ai_guess[letters] in word:
                        word_list_deepcopy.remove(word)
                        break
                    elif feedback_ai[letters] == 'y' and ai_guess[letters] not in word:
                        word_list_deepcopy.remove(word)
                        break
                    elif feedback_ai[letters] == 'y' and ai_guess[letters] == word[letters]:
                        word_list_deepcopy.remove(word)
                        break
                    elif feedback_ai[letters] == 'g' and word[letters] != ai_guess[letters]:
                        word_list_deepcopy.remove(word)
                        break
            ai_guess = random.choice(word_list_deepcopy)
            if ai_guess_count == 6: # reached max number of guesses
                ai_guess_count += 1
                print(self)
                return ai_guess_count
        ai_guess_count += 1
        # print("AI guess count: " + str(ai_guess_count))
        # print("last guess: " + ai_guess)
        self.user_words += [ai_guess]
        self.addMove(ai_guess) # need to add move because the while loop breaks once the ai_guess is correct
        print("AI board: ")
        print(self)
        return ai_guess_count

def main(game_word):
    '''Main function for Wordle'''
    board = Board(5,6)
    ai_board = Board(5,6)
    global_gameword = board.game_word
    ai_board.game_word = global_gameword
    # print("gameword: ", global_gameword)
    print("Welcome to Wordle: Human vs. AI! ")
    print("An AI will be playing at the same time as you. Let's see if you can beat it!")
    if yes("Would you like to play (y/n)? "):
        print("Here is your board: ")
        print(board)
        player_guess_count = play(board)
        ai_guess_count = ai_board.ai_hard()
        if player_guess_count > ai_guess_count: # player loses
            print("Nice try! Computers will always be smarter. The AI guessed it in: {ai_guess_count} guesses.".format(ai_guess_count = ai_guess_count))
        elif player_guess_count < ai_guess_count: #player wins
            print("Maybe humans do have a chance. The AI guessed it in {ai_guess_count} guesses. We lose this time...".format(ai_guess_count = ai_guess_count))
        elif player_guess_count == ai_guess_count and player_guess_count!= 7: # player ties with AI
            print("You got lucky! The AI also guessed it in {ai_guess_count} guesses.".format(ai_guess_count = ai_guess_count))
        elif player_guess_count == 7: #player does not guess correctly
            if ai_guess_count < player_guess_count: #ai does guess correctly
                print("You lose! The AI guesses it in: {ai_gest_count} guesses.".format(ai_guess_count))
            else: #ai also does not guess correctly
                print("Everyone loses! ")
        if yes("Would you like to play again (y/n)? "):
            main(global_gameword)
        else:
            print("Goodbye!")
    else:
        print("Goodbye!")
    return global_gameword

def play(self):
    '''Plays wordle and gives feedback on user input'''
    user_guess = ""
    guess_count = 0
    letter_bank = list()
    while self.feedback(user_guess) != "ggggg" and guess_count < 6:
        while True: # makes sure only a valid word is inputted
            user_guess = input("Please enter a five letter word: ").lower()
            if len(user_guess) == 5:
                if user_guess in word_list:
                    break
                else:
                    print("Please enter a valid five letter word. Try again...")
            else:
                print("Please enter a string of length five. Try again...")
        for i in user_guess:
            if i not in letter_bank:
                letter_bank.append(i)
        self.user_words += [user_guess]
        print("These are the letters you have guessed:", letter_bank)
        print(self)
        guess_count += 1
    print(self.feedback(user_guess))
    print("player guess:", guess_count)
    return guess_count

def yes(prompt):
    '''Asks user yes/no question and returns True if the answer is yes
    False if no.'''
    while True:
        answer = str(input(prompt)).lower()
        if answer == "yes" or answer == "y":
            return True
        elif answer == "no" or answer == "n":
            return False
        else:
            print("Please input a yes or no. Try again...")

if __name__ == '__main__': #automatically plays game if final.py is run
    main(global_gameword)
