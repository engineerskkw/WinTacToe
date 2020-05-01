from environments.tic_tac_toe.tic_tac_toe_engine import TicTacToeEngine
from reinforcement_learning.agents.monte_carlo_agent.monte_carlo_agent import MonteCarloAgent
from training_platform import EnvironmentServer
from training_platform import AgentClient

if __name__ == '__main__':
    server = EnvironmentServer(TicTacToeEngine(2, 3, 3))
    players = server.players
    p0 = players[0]
    p1 = players[1]

    c0 = AgentClient(MonteCarloAgent())
    c1 = AgentClient(MonteCarloAgent())

    server.join(c0, p0)
    server.join(c1, p1)

    for i in range(100):
        print(i)
        server.start()

    server.shutdown()