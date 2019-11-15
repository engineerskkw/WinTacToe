# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys
import os
REL_PROJECT_ROOT_PATH = "./../../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#


from environments.tic_tac_toe.tic_tac_toe_engine import TicTacToeEngine
from reinforcement_learning.agents.basic_mc_agent.basic_mc_agent import BasicAgent
from training_platform import EnvironmentServer
from training_platform import AgentClient

if __name__ == '__main__':
    server = EnvironmentServer(TicTacToeEngine(2, 3, 3))
    players = server.players
    p0 = players[0]
    p1 = players[1]

    c0 = AgentClient(BasicAgent())
    c1 = AgentClient(BasicAgent())

    server.join(c0, p0)
    server.join(c1, p1)

    for i in range(100):
        print(i)
        server.start()

    server.shutdown()

    # # Plot
    # agent_data = mces.agent1_G
    #
    # bin_size = 100
    # bins_number = int(np.floor(len(agent_data)/bin_size))
    # mean_returns = [np.mean(agent_data[i*bin_size:(i+1)*bin_size]) for i in range(bins_number)]
    # mean_returns.append(np.mean(agent_data[bins_number*bin_size:]))
    #
    # x = list(range(len(mean_returns)))
    # y = mean_returns
    # plt.scatter(x, y)
    # plt.ylabel(f'Mean Returns')
    # plt.xlabel('Episode bins (bin size: {bin_size})')
    # print("Mean Returns vs episodes:")
    # plt.show()
    #
    # x = np.array(agent_data)[-1000:-1]
    # n, bins, patches = plt.hist(x, bins='auto', density=True, facecolor='orange', alpha=1)
    # plt.xlabel('Return value')
    # plt.ylabel('Number of returns')
    # plt.title('Histogram of last 1000 Returns')
    # plt.grid(True)
    # plt.show()
    #
    # plt.plot(mces.epsilons)
    # plt.ylabel('Epsilon value')
    # plt.ylabel('Epsilon value')
    # print("Epsilones vs episodes")
    # plt.show()
    #
    # mdp = agent1.get_MDP()
    # # mdp.mdp_graph.view()
    # mdp.view()
    #
    # print("Last episode")
    # agent1.last_episode.view()
    #
    # print("SimpleAction-value function")
    # agent1.action_value.view()
    #
    # print("Policy")
    # agent1.policy.view()
    #
    # print("Returns for (SimpleState, SimpleAction) pairs")
    # agent1.returns.view()
    #
    # print("Model")
    # agent1.model.view()