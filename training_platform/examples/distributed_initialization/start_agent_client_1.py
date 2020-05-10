from training_platform.server.environment_server import EnvironmentServer
from training_platform import AgentClient
from reinforcement_learning.agents.monte_carlo_agent.monte_carlo_agent import MonteCarloAgent
from reinforcement_learning.agents.common_building_blocks.epsilon_strategy import CircleEpsilonStrategy

if __name__ == '__main__':
    server = EnvironmentServer()
    p = server.players[1]
    c = AgentClient(MonteCarloAgent(CircleEpsilonStrategy(starting_epsilon_value=0.1, exploration_part=0.7)))
    c.join(p)
    print("BaseAgent Client has joind server!")