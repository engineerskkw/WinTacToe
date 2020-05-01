from training_platform.server.environment_server import EnvironmentServer
from training_platform import AgentClient
from reinforcement_learning.agents.monte_carlo_agent.monte_carlo_agent import MonteCarloAgent

if __name__ == '__main__':
    server = EnvironmentServer()
    p = server.players[1]
    c = AgentClient(MonteCarloAgent())
    c.join(p)
    print("BaseAgent Client has joind server!")