# TODO: Restructure training

# #BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
# import sys, os
# REL_PROJECT_ROOT_PATH = "./../"
# ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
# ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
# sys.path.append(ABS_PROJECT_ROOT_PATH)
# #-------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

# import numpy as np
# import gym
# from parse import parse
# import matplotlib.pyplot as plt

# from src.extensions.games.tic_tac_toe.tic_tac_toe_logic import *
# from src.extensions.games.tic_tac_toe.tic_tac_toe import *
# from reinforcement_learning.agents.basic_agent import BasicAgent
# from monte_carlo_es import MonteCarloES

# # Initialization
# players = [Player('A', 0), Player('B', 1)]
# agent1 = Agent(env, players[0])
# agent2 = Agent(env, players[1])
# # agent2.policy = Policy(env) # Fixed, random policy
# mces = MonteCarloES(agent1, agent2)

# # Train
# mces.train(1000, initial_epsilon=0.3)

# # Plot
# agent_data = mces.agent1_G

# bin_size = 100
# bins_number = int(np.floor(len(agent_data)/bin_size))
# mean_returns = [np.mean(agent_data[i*bin_size:(i+1)*bin_size]) for i in range(bins_number)]
# mean_returns.append(np.mean(agent_data[bins_number*bin_size:]))

# x = list(range(len(mean_returns)))
# y = mean_returns
# plt.scatter(x, y)
# plt.ylabel(f'Mean Returns')
# plt.xlabel('Episode bins (bin size: {bin_size})')
# print("Mean Returns vs episodes:")
# plt.show()

# x = np.array(agent_data)[-1000:-1]
# n, bins, patches = plt.hist(x, bins='auto', density=True, facecolor='orange', alpha=1)
# plt.xlabel('Return value')
# plt.ylabel('Number of returns')
# plt.title('Histogram of last 1000 Returns')
# plt.grid(True)
# plt.show()

# plt.plot(mces.epsilons)
# plt.ylabel('Epsilon value')
# plt.ylabel('Epsilon value')
# print("Epsilones vs episodes")
# plt.show()

# mdp = agent1.get_MDP()
# # mdp.mdp_graph.view()
# mdp.view()

# print("Last episode")
# agent1.last_episode.view()

# print("Action-value function")
# agent1.action_value.view()

# print("Policy")
# agent1.policy.view()

# print("Returns for (State, Action) pairs")
# agent1.returns.view()

# print("Model")
# agent1.model.view()

