from ..scenes.tic_tac_toe_scene import TicTacToeScene
from ..util.tic_tac_toe_rewards import *
from ..engine import TicTacToeEngine
from pygame.locals import *
from gym import spaces
import gym

NOT_END = 0
END_BY_WIN = 1
END_BY_DRAW = 2


class TicTacToeBasicEnv(gym.Env):
	metadata = {'render.modes': ['human', 'app']}

	def __init__(self):
		pass

	def initialize(self, players, size, marks_required, app):
		self._params = (players, size, marks_required)
		self.env = TicTacToeEngine(players, size, marks_required)
		self.current_winnings = []

		self.observation_space = spaces.MultiDiscrete([size, size])
		self.action_space = spaces.MultiDiscrete([size, size])

		self.possible_actions = self.env.get_unoccupied_fields()

		self.next_step_done = NOT_END

		self._default_screen = None # TODO create default screen
		self._scene = TicTacToeScene(self)
		self.app = app

	def step(self, action, player):
		# End game case
		if self.next_step_done:
			state = self.env.board.board
			if self.next_step_done == END_BY_WIN:
				reward = LOOSE_REWARD
			if self.next_step_done == END_BY_DRAW:
				reward = TIE_REWARD
			return state, reward, True, {"metadata"}, None

		# Move
		x, y = action
		try:
			ple = self.env.current_player
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

		return state, reward, False, {"metadata"}, ple

	def reset(self):
		self.env = TicTacToeEngine(*self._params)
		self.current_winnings = []

		self.possible_actions = []
		self._regenerate_possible_actions()
		self.next_step_done = NOT_END
		self._scene = TicTacToeScene(self)

	def render(self, mode='human', screen=None):
		if mode == 'human':
			print(self.env.board.board)
		if mode == 'app':
			self._scene.render(screen if screen else self._default_screen)

	def handle_event(self, event):
		if event.type == MOUSEBUTTONUP:
			if self._scene.restart_button.contains_point(event.pos):
				self._scene.restart_button.on_pressed()
			elif self._scene.main_menu_button.contains_point(event.pos):
				self._scene.main_menu_button.on_pressed()
			else:
				buttons = sum(self._scene.buttons, [])
				for button in filter(lambda butt: butt.contains_point(event.pos), buttons):
					button.on_pressed()

	def regenerate_possible_actions(self):
		self.possible_actions = self.env.get_unoccupied_fields()
