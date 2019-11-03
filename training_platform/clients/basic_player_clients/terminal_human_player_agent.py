import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from abstract_agent import Agent
from parse import parse
import numpy as np

def pretty_print(state):
    representation = ''
    height, width = state.shape
    
    for h in range(height):
        for w in range(width):
            if state[h,w] == -1:
                representation += '#'
            elif state[h,w] == 0:
                representation += 'O'
            elif state[h,w] == 1:
                representation += 'X'
            else:
                print("Invalid mark code")
                raise
        if h < height-1:
            representation += '\n'
    print(representation)

class HumanPlayerAgent(Agent):
    def __init__(self):
        pass

    def step(self, state, allowed_actions):
        print("State:")
        pretty_print(state)
        while True:
            input_string = input("\nType move's coordinates in order y, x (i.e 1,2): ")
            print("\n")
            result = parse("{},{}", input_string)
            y = int(result[0])
            x = int(result[1])
            if (y,x) in allowed_actions:
                return y, x
            else:
                print("Invalid action, try again")

    def reward(self, reward):
        print(f"Received reward: {reward}")

    def exit(self, final_state):
        print(f"Game Over:")
        pretty_print(final_state)