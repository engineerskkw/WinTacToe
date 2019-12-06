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
from itertools import product


class LinearRegressionActionValue(BaseActionValue):
    MIN_PEN_WIDTH = 1
    MAX_PEN_WIDTH = 4

    def __init__(self, init_weights_zeros=False):
        self.weights = None
        self.init_weights_zeros=init_weights_zeros

    def __getitem__(self, key: tuple):
        assert len(key) == 2, f"Invalid key: {key}, should be tuple(BaseState, BaseAction)..."
        state, action = key
        features = self.__get_features(state, action)

        # print(f"features XD: {features}")

        # Lazy weights initialization
        if self.weights is None:
            self.weights = self.__init_weights(features.size)

        return float(np.dot(self.weights, features))

    def sample_update(self, **kwargs):
        state = kwargs['state']
        action = kwargs['action']
        step_size = kwargs['step_size']
        target = kwargs['target']

        if self.weights is None:
            self.weights = self.__init_weights(self.__get_features(state, action).size)

        # Stochastic gradient descent
        gradient = self.__gradient(state, action)
        self.weights = self.weights + step_size * (target - self[state, action]) * gradient

        # print(self.weights)

    def __get_features(self, state, action):
        # Additional [1] because there is also bias
        # TODO: implement flatten in state and action
        x = np.concatenate((state.flatten(), action.flatten()))
        additional_features = np.array([i[0] * i[1] for i in product(x, x)])
        final_features = np.concatenate((x, additional_features, [1])).reshape(-1, 1)
        norm = np.linalg.norm(final_features)

        return  final_features / norm

    def __init_weights(self, feature_size):
        tmp = np.zeros(feature_size) if self.init_weights_zeros else np.random.uniform(-0.01, 0.01, feature_size)
        tmp.reshape((1, -1))
        return tmp

    def __gradient(self, state, action):
        return self.__get_features(state, action).transpose()

    def max(self, state, action_space):
        # TODO: fix iteration over possibly infinite action_space
        if not action_space:
            return 0.
        expected_returns = [self.__getitem__((state, action)) for action in action_space.actions]
        return max(expected_returns)

    def argmax(self, state, action_space):
        # TODO: fix iteration over possibly infinite action_space
        if not action_space.actions:
            return {}

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
        if self.weights is None:
            graph.node('0', "Empty action value")
            return graph

        weights = self.weights.flatten()
        output_node_hash = str(uuid.uuid4())
        graph.node(output_node_hash, "Output node")
        for i in range(weights.size):
            feature_node_hash = str(uuid.uuid4())
            weight = weights[i]
            if not i == weights.size-1:
                feature_node_name = f"Feature {i}"
            else:
                feature_node_name = "Bias feature = 1"
            graph.node(feature_node_hash, feature_node_name)
            blue = int(linear_map(weight, 0, 255, weights))
            color = '#%02x%02x%02x' % (0, 0, blue)
            penwidth = str(linear_map(weight, self.MIN_PEN_WIDTH, self.MAX_PEN_WIDTH, weights))
            graph.edge(feature_node_hash, output_node_hash, label=str(weight),
                       color=color, penwidth=penwidth)
        return graph

    def _repr_svg_(self):
        return self._get_graph()._repr_svg_()

    def view(self):
        return self._get_graph().view()
