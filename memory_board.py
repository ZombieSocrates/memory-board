# Defines the MemoryBoard class for the implementation of 
# Memory that I am making

from math import floor
import numpy as np
from urllib.request import urlopen
from itertools import product

# Pulling a certain number of random words from
# this website will supply the content of the cards
word_url = "http://learncodethehardway.org/words.txt"
words = [word.strip() for word in urlopen(word_url).readlines()]

class MemoryBoard(object):
	'''
	MemoryBoard is the object that will be displayed as the user
	plays memory.  Attributes are as follows:

		* n_pairs: The number of matched pairs to play with. This is
		the ONLY attribute requiring user input.

		* rows: Number of rows in which the 2 * n_pairs cards in play
		will be organized in.  Calculated to best approximate a square layout.
		
		* columns: Number of columns in which the 2 * n_pairs cards in play
		will be organized in.  Calculated to best approximate a square layout.

		* board: A numpy matrix representing the physical board that the player
		interacts with.  Will be printed to the screen and updated with each
		turn of play.

		* pair_names: The actual names of the objects that the player needs to
		guess.  These are harvested at random from the url above
		
		* solution_dict: Represents how the cards are displayed on MemoryBoard.board.
		Will be used to supply the correct object for any card that a user "flips over."

	'''
	def __init__(self, n_pairs, rows= 0, columns= 0, board = None,
				 pair_names = None, solution_dict = None):
		self.n_pairs = n_pairs
		self.columns = columns 
		self.rows = rows
		self.board = board
		self.pair_names = pair_names
		self.solution_dict = solution_dict

	@property
	def columns(self):
		return self._columns

	# columns = the largest integer <= sqrt(total number of cards in play) that is also
	# a factor of total number of cards in play
	@columns.setter
	def columns(self,columns):
		area = 2 * self.n_pairs
		best_guess = floor(np.sqrt(area))
		while area % best_guess != 0:
			best_guess -= 1
		self._columns = int(best_guess)

	@property
	def rows(self):
		return self._rows

	# rows = total cards/columns 
	@rows.setter
	def rows(self, rows):
		self._rows = int((2 * self.n_pairs)/self.columns)
   
	@property
	def board(self):
		return self._board

	# board = a rows by columns np.matrix that defaults with all
	# 'X' values (representing backs of cards). 
	@board.setter
	def board(self, board):
		board_vals = np.repeat('X', repeats=2 * self.n_pairs)
		self._board = np.mat(board_vals, dtype = 'object').reshape((self.rows, self.columns))

	@property
	def pair_names(self):
		return self._pair_names

	# pair_names  = the words that will be underneath the X's in the 
	# MemoryBoard.board object.  SIDE NOTE/FUN FACT: np.random.choice()
	# is only available in numpy version >= 1.7
	@pair_names.setter
	def pair_names(self, pair_names):
		self._pair_names = np.random.choice(words, size = self.n_pairs, replace = False)
	
	@property
	def solution_dict(self):
		return self._solution_dict

	# solution_dict: randomly allocate two copies of each item in pair_names
	# to the total number of cards in the board.
	@solution_dict.setter
	def solution_dict(self, solution_dict):
		position_list = [b for b in product([i for i in range(self.rows)], [i for i in range(self.columns)])]
		card_names = np.repeat(self.pair_names, repeats = 2)
		np.random.shuffle(card_names)
		output = {}
		for i in range(len(position_list)):
			output[position_list[i]] = card_names[i]
		self._solution_dict = output
	
#Just for debugging 
if __name__ == '__main__':
	test_pairs = int(input('Number of pairs?' ))
	test1 = MemoryBoard(test_pairs)
	print(test1.rows)
	print(test1.columns)
	print(test1.board) 
	# Can i update the board in place?
	row_col = [int(b) for b in input('Choose card to flip by index: ').split()]
	value = test1.solution_dict[(row_col[0], row_col[1])]
	print('Value at position (%s, %s): %s' % (row_col[0], row_col[1], value))
	test1.board[row_col[0], row_col[1]] = value
	print(test1.board)	
