# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os

REL_PROJECT_ROOT_PATH = "./../../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

from graphviz import Digraph
import numpy as np
import uuid

from reinforcement_learning.agents.common.auxiliary_utilities import linear_map
from reinforcement_learning.base.base_action_value import BaseActionValue
from all_tests.mock.test_mock_state import MockState
from all_tests.mock.test_mock_action import MockAction


class LogisticRegressionActionValue(BaseActionValue):
    MIN_PEN_WIDTH = 1
    MAX_PEN_WIDTH = 4

    def __init__(self):
        self.weights = None

    def __getitem__(self, key: tuple):
        assert len(key) == 2, f"Invalid key: {key}, should be tuple(BaseState, BaseAction)..."
        state, action = key
        features = self.__get_features(state, action)

        # Lazy weights initialization
        if self.weights is None:
            self.weights = self.__init_weights(features.size)

        return float(np.dot(self.weights, features))

    def sample_update(self, **kwargs):
        state = kwargs['state']
        action = kwargs['action']
        step_size = kwargs['step_size']
        target = kwargs['target']

        old_estimate = self.__getitem__((state, action))
        gradient = self.__gradient(state, action)

        # Update rule for weights
        self.weights = self.weights + step_size * (target - old_estimate) * gradient

    def __get_features(self, state, action):
        # Additional [1] because there is also bias
        # TODO: implement flatten in state and action
        return np.concatenate((state.flatten, action.flatten, [1])).reshape(-1, 1)

    def __init_weights(self, feature_size, zeros=False):
        if zeros:
            tmp = np.zeros(feature_size)
        else:
            tmp = np.random.randint(feature_size)
        return tmp.reshape((1, -1))

    def __gradient(self, state, action):
        return self.__get_features(state, action).transpose()

    def max(self, state, action_space):
        # TODO: fix iteration over possibly infinite action_space
        expected_returns = [self.__getitem__((state, action)) for action in action_space.actions]
        return max(expected_returns)

    def argmax(self, state, action_space):
        # TODO: fix iteration over possibly infinite action_space
        max_action_value = self.max(state, action_space)
        return {action for action in action_space.actions if self.__getitem__((state, action)) == max_action_value}

    def action_returns(self, state, action_space):
        # TODO: fix iteration over possibly infinite action_space
        return {action: self.__getitem__((state, action)) for action in action_space.actions}

    def __str__(self):
        return str(self.weights)

    def __repr__(self):
        return self.__str__()

    def _get_graph(self):
        graph = Digraph()
        output_node_hash = str(uuid.uuid4())
        graph.node(output_node_hash, "Output node")
        for i in range(self.weights.size):
            feature_node_hash = str(uuid.uuid4())
            weight = self.weights[i]
            if not i == self.weights.size-1:
                feature_node_name = f"Feature {i}"
            else:
                feature_node_name = "Bias feature = 1"
            graph.node(feature_node_hash, feature_node_name)
            blue = int(linear_map(weight, 0, 255, self.weights))
            color = '#%02x%02x%02x' % (0, 0, blue)
            penwidth = str(linear_map(weight, self.MIN_PEN_WIDTH, self.MAX_PEN_WIDTH, self.weights))
            graph.edge(feature_node_hash, output_node_hash, label=str(weight),
                       color=color, penwidth=penwidth)
        return graph

    def _repr_svg_(self):
        return self._get_graph()._repr_svg_()

    def view(self):
        return self._get_graph().view()

if __name__ == '__main__':
    # Logistic regression action-value test
    av = LazyTabularActionValue()
    print(av)
    #
    s = MockState([[-1, -1], [-1, 1]])

    a1 = MockAction([0, 0])
    a2 = MockAction([0, 1])
    a3 = MockAction([1, 0])

    av[s, a1] = 6
    av[s, a2] = 0.8
    av[s, a3] = -10

    print(av)
    # print(av.action_returns(s))
    # av.view()
    # print(s)
