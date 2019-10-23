import numpy as np
from itertools import cycle

from state import State


class MonteCarloES:
    def __init__(self, agent1, agent2):
        self.agent1 = agent1
        self.agent2 = agent2
        self.agent1_G = []
        self.agent2_G = []
        self.epsilons = []

    def train(self, episodes_no=1, initial_epsilon=0.3):
        for i in range(episodes_no):
            epsilon = np.e ** (-i / episodes_no * 5) * initial_epsilon  # Epsilon decaying
            self.epsilons.append(epsilon)  # Register epsilon for plotting purpose

            self.gen_episode(self.agent1, self.agent2, epsilon)
            self.agent1_G.append(self.pass_episode(self.agent1))
            self.agent2_G.append(self.pass_episode(self.agent2))

    def gen_episode(self, agent1, agent2, epsilon):
        # Reset agents' episodes
        agents = [agent1, agent2]
        for a in agents:
            a.reset_episode()

        # Players queue
        agents = cycle(agents)
        current_agent = next(agents)

        # Initialize environment
        env = agent1.env
        players = [agent1.player, agent2.player]
        size = 3
        marks_required = 3
        env.initialize(players, size, marks_required)

        # Generate episode
        done = False
        initial_state = State(env.get_current_state())
        #         initial_state = State(env.random_initial_state()) # Random state due to Exploring Starts approach
        state, done = current_agent.random_step(initial_state)  # Random action due to Exploring Starts approach
        while not done:
            current_agent = next(agents)
            state, done = current_agent.step(state, epsilon)

    #         current_agent = next(agents)

    def pass_episode(self, agent):
        episode = agent.last_episode
        gamma = 0.9  # Discount factor
        G = 0  # Episode's accumulative discounted total reward/return
        steps_no = len(episode) // 2
        for t in reversed(range(steps_no)):
            S, A = episode[2 * t]  # This step's (state, action) pair
            R = episode[2 * t + 1]  # This step's reward

            G = gamma * G + R  # Calculate discounted return

            # Update rule according to the Monte Carlo first-step approach
            if not (S, A) in episode[0:2 * t]:
                # Policy evaluation
                agent.returns[S, A].append(G)
                #                 # Improve only policy of the first agent
                #                 if agent.player.name == agent1.player.name:
                #                     agent.action_value[S,A] = np.mean(agent.returns[S,A])
                agent.action_value[S, A] = np.mean(agent.returns[S, A])  # Improve policy of both agents
                # Greedy policy improvement in the background (as a consequence of action_value change)
        #                 agent.policy[S] = agent.action_value.argmax_a(S)
        return G
