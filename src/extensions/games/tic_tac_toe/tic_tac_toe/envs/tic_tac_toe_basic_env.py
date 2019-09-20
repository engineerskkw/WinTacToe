import gym
from gym import error, spaces, utils
from gym.utils import seeding
import random


# Workaround import
import sys
sys.path.insert(1, '../../..')
from src.extensions.games.tic_tac_toe.tic_tac_toe_logic import *

EVERY_ACTION_REWARD = -1
WIN_REWARD = 10
LOOSE_REWARD = -10
TIE_REWARD = 0

NOT_END = 0
END_BY_WIN = 1
END_BY_DRAW = 2

class TicTacToeBasicEnv(gym.Env):
	metadata = {'render.modes': ['human']}

	def __init__(self):
		pass

	def initialize(self, players, size, marks_required):
		self.players = players
		self.size = size
		self.marks_required = marks_required

		self.env = TicTacToeLogic(players, size, marks_required)
		self.current_winnings = []

		self.observation_space = spaces.MultiDiscrete([size, size])
		self.action_space = spaces.MultiDiscrete([size, size])

		self.possible_actions = []
		self._regenerate_possible_actions()

		self.next_step_done = NOT_END

	def step(self, action, player):
		# End game case
		if self.next_step_done:
			state = self.env.board.board
			if self.next_step_done == END_BY_WIN:
				reward = LOOSE_REWARD
			if self.next_step_done == END_BY_DRAW:
				reward = TIE_REWARD
			return state, reward, True, {"metadata"}

		# Move
		x,y = action
		try:
			self.env.place_mark(x, y)
			state = self.env.board.board
		except IndexError as error:
			print("These are not valid coordinates...\n")
		self._regenerate_possible_actions()

		self.current_winnings = self.env.gather_winnings()
		# Win/loose case
		if self.current_winnings:
			self.next_step_done = END_BY_WIN
			reward = WIN_REWARD
		# Draw/no more moves case
		elif self.possible_actions == []:
			self.next_step_done = END_BY_DRAW
			reward = TIE_REWARD
		else:
			reward = EVERY_ACTION_REWARD

		
		return state, reward, False, {"metadata"}

	def reset(self):
		self.env = TicTacToeLogic(self.players, self.size, self.marks_required)

	def render(self, mode='human'):
		if mode == 'human':
			print(self.env.board.board)

	def get_current_state(self):
		return self.env.board.board

	def random_initial_state(self):
		### Uniform random initialization, but without
		# Game-endind or illegal(win of both players) states

		# All possible players' marks and empty mark
		players_marks = [-1]
		for p in self.env.players:
			players_marks.append(p.mark)

		# Random fields filling order
		coords = []
		size = self.env.board.size
		for v in range(size):
			for h in range(size):
				coords.append((v,h))

		random.shuffle(coords)
		n = random.randint(0,len(coords)) # Number of fields to fill

		# Random fields value
		for i in range(n):
			v,h = coords[i]
			random_mark = random.choice(players_marks)
			self.env.board.place_mark(v,h,random_mark)
			if self.env.gather_winnings():
				self.env.board.board[v,h] = -1

		# Check all fields filled
		# if so, then randomly unmark one of them
		all_filled = True
		for v in range(size):
			for h in range(size):
				if self.env.board.board[v,h] == -1:
					all_filled = False
					break

		if all_filled:
			v = random.randint(0,size-1)
			h = random.randint(0,size-1)
			self.env.board.board[v,h] = -1

		self._regenerate_possible_actions()

		return self.env.board.board

	def _regenerate_possible_actions(self):
		self.possible_actions = []
		board = self.env.board.board
		height, width = board.shape
		for h in range(height):
			for v in range(width):
				if board[h,v] == -1:
					self.possible_actions.append([h, v])

	# def close(self):
	# 	pass

# Example

# import gym
# from tic_tac_toe_logic import *

# env = gym.make('tic_tac_toe:tictactoe-v0')
# players = [Player('A', 0), Player('B', 1)]
# marks_required = 3
# size = 5
# env.initialize(players, size, marks_required)
# env.render()

# s, r, d, m = env.step(env.action_space.sample(), players[0])

