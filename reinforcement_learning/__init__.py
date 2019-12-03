# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys
import os
REL_PROJECT_ROOT_PATH = "./../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

# Abstract agent for loading purpose
from reinforcement_learning.base.base_agent import BaseAgent

# Concrete agents
from reinforcement_learning.agents.basic_mc_agent.basic_mc_agent import BasicAgent
from reinforcement_learning.agents.random_agent.random_agent import RandomAgent
from reinforcement_learning.agents.n_step_agent.n_step_agent import NStepAgent
from reinforcement_learning.agents.q_learning_agent.q_learning_agent import QLearningAgent

# Training class
from reinforcement_learning.common.simple_training import SimpleTraining
