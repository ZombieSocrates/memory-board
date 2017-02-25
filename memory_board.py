# Defines the MemoryBoard class for the implementation of 
# Memory that I am making for ex45.py

from math import floor
import numpy as np
from urllib import urlopen

# Pulling a certain number of random words from
# this website will supply the content of the cards
word_url = "http://learncodethehardway.org/words.txt"
words = [word.strip() for word in urlopen(word_url).readlines()]

class MemoryBoard(object):

    def __init__(self, n_pairs, rows=0, columns=0,\
 		 board = None, pair_names = None, \
		 position_dict = None):
        self.n_pairs = n_pairs
	self.columns = columns 
	self.rows = rows
	self.board = board
	self.pair_names = pair_names
	self.position_dict = position_dict

    @property
    def columns(self):
	return self.__columns

    @columns.setter
    def columns(self,columns):
	area = 2 * self.n_pairs
	best_guess = floor(np.sqrt(area))
	while area % best_guess != 0:
	    best_guess -= 1
        self.__columns = int(best_guess)

    @property
    def rows(self):
        return self.__rows				

    @rows.setter
    def rows(self, rows):
	self.__rows = (2 * self.n_pairs)/self.columns
   
    @property
    def board(self):
	return self.__board

    @board.setter
    def board(self, board):
	board_vals = np.repeat('X', repeats=2 * self.n_pairs)
	self.__board = np.mat(board_vals).reshape((self.rows, self.columns))

    @property
    def pair_names(self):
	return self.__pair_names

    @pair_names.setter
    def pair_names(self, pair_names):
	# Version of numpy I was originally using came out
	# before np.random.choice was an option. the while loop
	# ensures that we sample without replacement
	random_indices = np.sort(np.random.randint(0, len(words),\
					   size = self.n_pairs))
	unique_test = np.sort(np.unique(random_indices))
	while np.array_equal(random_indices,unique_test) is False:
	    random_indices = np.sort(np.random.randint(0, len(words),\
					   size = self.n_pairs))
	    unique_test = np.sort(np.unique(random_indices))        
	self.__pair_names = [words[i] for i in random_indices]

#Just for debugging 
if __name__ == '__main__':
    test1 = MemoryBoard(10)
    print(test1.rows)
    print(test1.columns)
    print(test1.board) 
    print(test1.pair_names)	
