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
import tensorflow as tf

from reinforcement_learning.agents.common.auxiliary_utilities import linear_map
from reinforcement_learning.base.base_action_value import BaseActionValue
import time



class NeuralNetworkActionValue(BaseActionValue):
    MIN_PEN_WIDTH = 1
    MAX_PEN_WIDTH = 4

    def __init__(self, init_weights_zeros=False):
        self.model = None

    def __getitem__(self, key: tuple):
        start = time.time()
        assert len(key) == 2, f"Invalid key: {key}, should be tuple(BaseState, BaseAction)..."
        state, action = key
        features = self.__get_features(state, action)

        # Lazy model initialization
        if self.model is None:
            self.model = self.__init_model(features.size)

        prediction = self.model.predict(np.array([features]))[0, 0]
        end = time.time()
        print(f"getitem time: {end - start}")
        return prediction

    def sample_update(self, **kwargs):
        start = time.time()
        state = kwargs['state']
        action = kwargs['action']
        step_size = kwargs['step_size']
        target = kwargs['target']

        features = self.__get_features(state, action)

        # Lazy model initialization
        if self.model is None:
            self.model = self.__init_model(features.size)

        # Stochastic gradient descent
        single_example_dataset_x = np.array([features])
        single_example_dataset_y = np.array([target])

        tf.keras.backend.set_value(self.model.optimizer.lr, step_size)
        self.model.train_on_batch(single_example_dataset_x, single_example_dataset_y)
        end = time.time()
        print(f"update time: {end-start}")

    def __init_model(self, feature_size):
        model = tf.keras.models.Sequential([
                tf.keras.layers.Dense(15, input_dim=feature_size, activation='relu'),
                tf.keras.layers.Dropout(0.2),
                # tf.keras.layers.Dense(200, activation='relu'),
                # tf.keras.layers.Dropout(0.2),
                # tf.keras.layers.Dense(150, activation='relu'),
                # tf.keras.layers.Dropout(0.2),
                tf.keras.layers.Dense(1)
            ])
        model.compile(optimizer='adam',
                      loss='mean_squared_error',
                      metrics=['accuracy'])
        return model

    def __get_features(self, state, action):
        # No additional [1] because bias is implemented by tensorflow
        features = np.concatenate((state.flatten(), action.flatten()))
        normalized_features = features / np.linalg.norm(features)
        return normalized_features

    def max(self, state, action_space):
        # TODO: fix iteration over possibly infinite action_space
        if not action_space:
            return 0.
        expected_returns = [self[state, action] for action in action_space.actions]
        return max(expected_returns)

    def argmax(self, state, action_space):
        # TODO: fix iteration over possibly infinite action_space
        if not action_space.actions:
            return {}

        max_action_value = self.max(state, action_space)
        return {action for action in action_space.actions if self[state, action] == max_action_value}

    def action_returns(self, state, action_space):
        # TODO: fix iteration over possibly infinite action_space
        return {action: self[state, action] for action in action_space.actions}

    def __str__(self):
        return str(self.model)

    def __repr__(self):
        return self.__str__()

    def _get_graph(self):
        # graph = Digraph()
        # if self.weights is None:
        #     graph.node('0', "Empty action value")
        #     return graph
        #
        # weights = self.weights.flatten()
        # output_node_hash = str(uuid.uuid4())
        # graph.node(output_node_hash, "Output node")
        # for i in range(weights.size):
        #     feature_node_hash = str(uuid.uuid4())
        #     weight = weights[i]
        #     if not i == weights.size-1:
        #         feature_node_name = f"Feature {i}"
        #     else:
        #         feature_node_name = "Bias feature = 1"
        #     graph.node(feature_node_hash, feature_node_name)
        #     blue = int(linear_map(weight, 0, 255, weights))
        #     color = '#%02x%02x%02x' % (0, 0, blue)
        #     penwidth = str(linear_map(weight, self.MIN_PEN_WIDTH, self.MAX_PEN_WIDTH, weights))
        #     graph.edge(feature_node_hash, output_node_hash, label=str(weight),
        #                color=color, penwidth=penwidth)
        # return graph
        pass

    def _repr_svg_(self):
        # return self._get_graph()._repr_svg_()
        pass

    def view(self):
        # return self._get_graph().view()
        pass
