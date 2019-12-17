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

from itertools import product


class NeuralNetworkActionValue(BaseActionValue):
    MIN_PEN_WIDTH = 1
    MAX_PEN_WIDTH = 4

    def __init__(self, init_weights_zeros=False):
        self.model = None
        self.optimizer = tf.keras.optimizers.SGD(learning_rate=0.3)
        self.train_loss_results = []

    def __getitem__(self, key: tuple):
        start = time.time()
        assert len(key) == 2, f"Invalid key: {key}, should be tuple(BaseState, BaseAction)..."
        state, action = key
        features = self.__get_features(state, action)

        # Lazy model initialization
        if self.model is None:
            self.model = self.__init_model(features.size)

        start = time.perf_counter()
        x = self.model(np.array([features]))[0, 0]
        end = time.perf_counter()

        # print(f"predict time: {end-start}")

        return x

    def sample_update(self, **kwargs):
        start = time.time()
        state = kwargs['state']
        action = kwargs['action']
        step_size = kwargs['step_size']
        target = kwargs['target']

        # tf.keras.backend.set_value(self.model.optimizer.lr, step_size)

        features = self.__get_features(state, action)

        # Lazy model initialization
        if self.model is None:
            self.model = self.__init_model(features.size)

        # Stochastic gradient descent
        single_example_dataset_x = np.array([features])
        single_example_dataset_y = np.array([target])


        start = time.perf_counter()
        loss, grads = self._grad(single_example_dataset_x, single_example_dataset_y)
        self.optimizer.apply_gradients(zip(grads, self.model.trainable_variables))

        self.train_loss_results.append(loss)
        end = time.perf_counter()

        # print(f"update time: {end-start}")

        # tf.keras.backend.set_value(self.model.optimizer.lr, step_size)
        # start = time.time()
        # self.model.fit(single_example_dataset_x, single_example_dataset_y, verbose=0, epochs=1)
        # end = time.time()
        # # print(f"update time: {end-start}")

    def __init_model(self, feature_size):
        model = tf.keras.models.Sequential([
                tf.keras.layers.Dense(100, input_dim=feature_size, activation='relu'),
                # tf.keras.layers.Dropout(0.2),
                tf.keras.layers.Dense(200, activation='relu'),
                # tf.keras.layers.Dropout(0.2),
                tf.keras.layers.Dense(100, activation='relu'),
                # tf.keras.layers.Dropout(0.2),
                tf.keras.layers.Dense(1)
            ])

        return model

    # def _init_optimizer(self, step_size):
    #     return tf.keras.optimizers.SGD(learning_rate=step_size)

    # def __get_features(self, state, action):
    #     # No additional [1] because bias is implemented by tensorflow
    #     features = np.concatenate((state.flatten(), action.flatten()))
    #     normalized_features = features / np.linalg.norm(features)
    #     return normalized_features

    def __get_features(self, state, action):
        # TODO: implement flatten in state and action
        x = np.concatenate((state.flatten(), action.flatten()))
        additional_features = np.array([i[0] * i[1] for i in product(x, x)])
        final_features = np.concatenate((x, additional_features))
        norm = np.linalg.norm(final_features)

        return final_features / norm

    def max(self, state, action_space):
        # TODO: fix iteration over possibly infinite action_space
        if not action_space:
            return 0.

        available_state_actions = [self.__get_features(state, action) for action in action_space.actions]

        if self.model is None:
            print("initialization")
            self.model = self.__init_model(available_state_actions[0].size)

        expected_returns = self.model(tf.constant(np.array(available_state_actions)))
        return max(expected_returns)

    def argmax(self, state, action_space):
        # TODO: fix iteration over possibly infinite action_space
        # TODO: always returns single element set <- its wrong xd
        if not action_space.actions:
            return {}

        available_state_actions = [self.__get_features(state, action) for action in action_space.actions]

        if self.model is None:
            print("initialization")
            self.model = self.__init_model(available_state_actions[0].size)

        values = self.model(tf.constant(np.array(available_state_actions)))

        max_action_index = np.argmax(values)

        return {list(action_space.actions)[max_action_index]}

    def action_returns(self, state, action_space):
        # TODO: fix iteration over possibly infinite action_space
        return {action: self[state, action] for action in action_space.actions}

    def __str__(self):
        return str(self.model)

    def __repr__(self):
        return self.__str__()

    def _loss(self, single_dataset_features, single_dataset_target_update):
        single_dataset_old_estimate = self.model(tf.constant(single_dataset_features))

        return tf.keras.losses.mean_squared_error(
            y_true=single_dataset_target_update,
            y_pred=single_dataset_old_estimate
        )

    def _grad(self, single_dataset_features, single_dataset_target_update):
        with tf.GradientTape() as tape:
            loss_value = self._loss(single_dataset_features, single_dataset_target_update)
        return loss_value, tape.gradient(loss_value, self.model.trainable_variables)

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
