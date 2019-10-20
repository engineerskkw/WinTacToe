import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from abstract_agent import Agent
from parse import parse


class HumanPlayerAgent(Agent):
    def __init__(self):
        pass

    def step(self, state, allowed_actions):
        print("[Agent]: State:")
        print(state)
        input_string = input("\nType move's coordinates in order y, x (i.e 1,2): ")
        print("\n")
        result = parse("{},{}", input_string)
        y = int(result[0])
        x = int(result[1])
        return y, x

    def reward(self, reward):
        print(f"[Agent]: Received reward: {reward}")

    def exit(self, final_state):
        print(f"[Agent]: Game Over:")
        print(final_state)