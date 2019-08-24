import gym
from gym import error, spaces, utils
from gym.utils import seeding


# Workaround import
import sys
sys.path.insert(1, '../../..')
from tic_tac_toe_logic import *

INVALID_ACTION_REWARD = -10
EVERY_ACTION_REWARD = -1
WIN_REWARD = 10
LOOSE_REWARD = -10

class TicTacToeBasicEnv(gym.Env):
	metadata = {'render.modes':['human']}

	def __init__(self):
		pass

	def initialize(self, players, size, marks_required):
		self.env = TicTacToeLogic(players, size, marks_required)
		self.current_winnings = []

		self.observation_space = spaces.MultiDiscrete([size, size])
		self.action_space = spaces.MultiDiscrete([size, size])

	def step(self, action, player):
		x,y = action

		reward = 0
		reward += EVERY_ACTION_REWARD

		try:
			if not self.env.place_mark(x, y):
				reward += INVALID_ACTION_REWARD
		except IndexError as error:
			print("These are not valid coordinates...\n")

		state = self.env.board.board
		done = False

		self.current_winnings = self.env.gather_winnings()
		if self.current_winnings:
			done = True
			if player in self.current_winnings:
				reward += WIN_REWARD
			else:
				reward += LOOSE_REWARD

		return state, reward, done, {"metadata"}

	def reset(self):
		self.env = TicTacToeLogic(players, size, marks_required)

	def render(self, mode='human'):
		if mode == 'human':
			print(self.env.board.board)

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

