import abstract_logic
import numpy as np
from itertools import chain, cycle


class Player:
	def __init__(self, name, mark):
		self.name = name
		self.mark = mark


class Winning:
	def __init__(self, mark, starting_point, ending_point):
		self.mark = mark
		self.starting_point = starting_point # tuple
		self.ending_point = ending_point # tuple

	def __str__(self):
		return str(self.mark) + ", start: " + str(self.starting_point) + ", end: " + str(self.ending_point)


class Board:
	def __init__(self, size, marks_required):
		self.size = size
		self.marks_required = marks_required
		self.board = np.full((size, size), -1) # -1 - puste miejsce

	def place_mark(self, x, y, mark):
		self.board[x][y] = mark

	def gather_winnings(self):
	winnings = []

	for i in range(size - marks_required + 1):
		for j in range(size - marks_required + 1):
			subboard = board[i:i+marks_required, j:j+marks_required]
			winnings += _check_subboard(subboard, (i, j))

	return chain.from_iterable(winnings)

	# private methods
	def _check_subboard(self, subboard, top_left):
		winnings = []
		shape = subboard.shape[0]

		#rows
		for i in range(shape):
			if _check_line(subboard[i]):
				mark = subboard[i][0]
				starting_point = (top_left[0] + i, top_left[1])
				ending_point = (top_left[0] + i, top_left[1] + shape - 1)

				yield Winning(mark, starting_point, ending_point)

		#columns
		for j in range(shape):
			if _check_line(subboard[:, j]):
				mark = subboard[:, j][0]
				starting_point = (top_left[0], top_left[1] + j)
				ending_point = (top_left[0] + shape - 1, top_left[1] + j)

				yield Winning(mark, starting_point, ending_point)

		#main_diagonal
		main_diag = np.diag(subboard)
		if _check_line(main_diag):
			mark = main_diag[0]
			starting_point = (top_left[0], top_left[1])
			ending_point = (top_left[0] + shape - 1, top_left[1] + shape - 1)

			yield Winning(mark, starting_point, ending_point)

		#second_diagonal
		second_diag = np.diag(np.flip(subboard, 1))
		if _check_line(second_diag):
			mark = second_diag[0]
			starting_point = (top_left[0], top_left[1] + shape - 1)
			ending_point = (top_left[0] + shape - 1, top_left[1])

			yield Winning(mark, starting_point, ending_point)

	def _check_line(line):
		if not np.any(line == -1) and np.all(line == line[0]):
			return True
		

class TicTacToeLogic(AbstractLogic):
	def __init__(self, players, size, marks_required):
		self.players = players
		self.player_generator = cycle(players)
		self.current_player = players[0]

		self.board_size = board_size
		self.board = Board(board_size, marks_required)

	def place_mark(self, x, y):
		self.board.place_mark(x, y, self.current_player.mark)
		self.current_player = next(player_generator)

	def gather_winnings(self):
		return self.board.gather_winnings()

	def get_current_state(self):
		return self.board.board

	def main_loop(self):
		current_winnings = []

		while not current_winnings:
			x, y = input(str(self.current_player.name) "'s turn... enter coordinates (e.g 1, 2):")
			self.place_mark(x, y)
			current_winnings = list(gather_winnings())

		winning_mark = current_winnings[0].mark
		winning_player = filter(lambda player: player.mark = winning_mark, self.players)[0]

		print(str(winning_player.name) + "won!")
