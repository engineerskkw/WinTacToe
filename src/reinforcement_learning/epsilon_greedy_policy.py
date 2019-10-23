import random

from state import State
from action import Action
from action_value import ActionValue


class EpsilonGreedyPolicy:
    def __init__(self, env, action_value, epsilon):
        self.action_value = action_value
        self.env = env
        self.epsilon = epsilon

    # Action-value and epsilon based action choosing
    def __getitem__(self, state):
        if random.random() >= self.epsilon:
            action = self.action_value.argmax_a(state)
            if action != Action([]):
                return action
        if self.env.possible_actions:
            return Action(random.choice(self.env.possible_actions))
        return Action([])

    # Representations
    def __str__(self):
        return self.action_value.__str__()

    def __repr__(self):
        return self.__str__()

    def _repr_svg_(self):
        return self.action_value._repr_svg_()

    def view(self):
        return self.action_value.view()


av = ActionValue()

s = State([[-1, -1], [-1, 1]])

a1 = Action([0, 0])
a2 = Action([0, 1])
a3 = Action([1, 0])

av[s, a1] = 6
av[s, a2] = 2.9
av[s, a3] = -10

egp = EpsilonGreedyPolicy(None, av, 0.3)

print(egp)
egp.view()