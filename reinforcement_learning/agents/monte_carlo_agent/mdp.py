from graphviz import Digraph
import numpy as np

from reinforcement_learning.agents.auxiliary_utilities import linear_map


class MDP:
    MIN_PEN_WIDTH = 1
    MAX_PEN_WIDTH = 4

    def __init__(self, model, action_value, policy):
        self.model = model
        self.action_value = action_value

        mdp_graph = Digraph()

        model_dict = self.model.model_dict
        for state, actions in model_dict.items():
            # State node
            mdp_graph.attr('node', shape='doublecircle', style='', fontcolor='black')
            state_hash = str(hash(state))
            mdp_graph.node(state_hash, str(state))
            for action, next_states in actions.items():
                # Action node
                mdp_graph.attr('node', shape='circle', style='filled', color='black',
                               fontcolor='white')
                action_hash = str(hash(action)) + state_hash
                mdp_graph.node(action_hash, str(action))

                this_action_value = np.round(self.action_value[state, action], 2)
                action_values = self.action_value.action_value_dict[state].values()
                red = int(linear_map(this_action_value, 0, 255, action_values))
                color = '#%02x%02x%02x' % (red, 0, 0)
                penwidth = str(linear_map(this_action_value, self.MIN_PEN_WIDTH,
                                          self.MAX_PEN_WIDTH, action_values))
                mdp_graph.edge(state_hash,
                               action_hash,
                               label=str(this_action_value),
                               color=color, penwidth=penwidth)

                # Calculate sum of all visits numbers
                all_visits_no = sum(next_states.values())
                for next_state, visits_number in next_states.items():
                    # Next state node
                    mdp_graph.attr('node', shape='doublecircle', style='', fontcolor='black')
                    next_state_hash = str(hash(next_state))
                    mdp_graph.node(next_state_hash, str(next_state))

                    visits_percentage = np.round(visits_number / all_visits_no * 100, 2)
                    label = f"{visits_number} ({visits_percentage}%)"
                    blue = int(linear_map(visits_number, 0, 255, next_states.values()))
                    color = '#%02x%02x%02x' % (0, 0, blue)
                    penwidth = str(linear_map(visits_number, self.MIN_PEN_WIDTH, self.MAX_PEN_WIDTH,
                                              next_states.values()))
                    mdp_graph.edge(action_hash, next_state_hash, label=label,
                                   color=color, penwidth=penwidth)

        self.mdp_graph = mdp_graph

    def _repr_svg_(self):
        return self.mdp_graph._repr_svg_()

    def view(self):
        return self.mdp_graph.view()