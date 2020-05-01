import numpy as np
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod
from copy import deepcopy


class BaseEpsilonStrategy(ABC):
    def __init__(self, starting_epsilon_value, exploration_part):
        self.starting_epsilon_value = starting_epsilon_value
        self.exploration_part = exploration_part

        # TODO: Not lazy init no of episodes, its disgusting
        self.no_of_episodes = None

        self.x = None
        self.y = None
        self.iterator = None

    def __next__(self):
        return next(self.iterator)

    @abstractmethod
    def init_no_of_episodes(self, no_of_episodes):
        pass

    def visualize(self):
        plt.plot(self.x, self.y)
        plt.show()

    def normalize(self, base_shape_x, base_shape_y):
        first_part_x = deepcopy(base_shape_x)
        first_part_y = deepcopy(base_shape_y)

        base_ending_x = first_part_x[-1]
        base_max_value = np.max(first_part_y)

        # arguments between 0 and exploration_part normalizing
        first_part_x /= base_ending_x
        first_part_x *= self.exploration_part

        # values between 0 and starting_epsilon_value normalizing
        first_part_y /= base_max_value
        first_part_y *= self.starting_epsilon_value

        return first_part_x, first_part_y

    def add_ending(self, normalized_x, normalized_y):
        # adding non exploration part
        non_exploration_episodes = self.no_of_episodes - int(self.no_of_episodes * self.exploration_part)
        second_part_x = np.linspace(self.exploration_part, 1, non_exploration_episodes)
        second_part_y = np.zeros(non_exploration_episodes)

        full_x = np.concatenate([normalized_x, second_part_x])
        full_y = np.concatenate([normalized_y, second_part_y])

        return full_x, full_y


class CircleEpsilonStrategy(BaseEpsilonStrategy):
    def __init__(self, starting_epsilon_value, exploration_part):
        super().__init__(starting_epsilon_value, exploration_part)

    def init_no_of_episodes(self, no_of_episodes):
        self.no_of_episodes = no_of_episodes

        r = 1
        base_shape_x = np.linspace(0, r, int(self.exploration_part * self.no_of_episodes))
        base_shape_y = np.sqrt(r**2 - base_shape_x**2)
        normalized_x, normalized_y = self.normalize(base_shape_x, base_shape_y)

        self.x, self.y = self.add_ending(normalized_x, normalized_y)
        self.iterator = iter(self.y)


class DecayingSinusEpsilonStrategy(BaseEpsilonStrategy):
    def __init__(self, starting_epsilon_value, exploration_part):
        super().__init__(starting_epsilon_value, exploration_part)

    def init_no_of_episodes(self, no_of_episodes):
        self.no_of_episodes = no_of_episodes

        starting_base_x = 1.1
        ending_base_x = 30 * np.pi
        convex_factor = 1

        base_shape_x = np.linspace(starting_base_x, ending_base_x, int(self.exploration_part * self.no_of_episodes))
        base_shape_y = np.sin(base_shape_x) ** 2 / (base_shape_x ** convex_factor)
        normalized_x, normalized_y = self.normalize(base_shape_x, base_shape_y)

        self.x, self.y = self.add_ending(normalized_x, normalized_y)
        self.iterator = iter(self.y)


class ConstantEpsilonStrategy(BaseEpsilonStrategy):
    def __init__(self, starting_epsilon_value, exploration_part=None):
        super().__init__(starting_epsilon_value, exploration_part)

    def init_no_of_episodes(self, no_of_episodes):
        self.x = np.linspace(0, 1, no_of_episodes)
        self.y = np.repeat(self.starting_epsilon_value, self.x.size)

        self.iterator = iter(self.y)
