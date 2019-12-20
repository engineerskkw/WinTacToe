# WinTacToe
WinTacToe is a system for training **reinforcement learning** agents to play tic-tac-toe-related games.
It consists of the following elements:
* Multiple, diverse game environments
* RL agents of various architectures and levels of advancement
* **Human player interface** which allow to play game with the chosen agent(s)

Futhermore WinTacToe allows to analyse agents



## Beginners guide
### Preambula
```python
# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys
import os

REL_PROJECT_ROOT_PATH = "./../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#
```

### Imports
```python
# Engine
from environments.tic_tac_toe.tic_tac_toe_engine import TicTacToeEngine

#Agents
from reinforcement_learning.base.base_agent import BaseAgent
from reinforcement_learning.new_agents.n_step_agent.n_step_agent import NStepAgent
from reinforcement_learning.new_agents.random_agent.random_agent import RandomAgent
from reinforcement_learning.new_agents.dqn_agent.dqn_agent import DQNAgent

# Agents building blocks
from reinforcement_learning.new_agents.common.epsilon_strategy import ConstantEpsilonStrategy, CircleEpsilonStrategy, DecayingSinusEpsilonStrategy

# Training
from reinforcement_learning.common.simple_training import SimpleTraining

# Agents Database
from reinforcement_learning.agents_database.agents_db import AgentsDB

# To avoid warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
```
### Starting bot vs bot vs ... vs bot training with any engine:

To start a training you need an engine:
```python
engine = TicTacToeEngine(2, 3, 3)
```

...and agents, so you can create them:
```python
agents = [NStepAgent(n=5,
                     step_size=0.1,
                     epsilon_strategy=CircleEpsilonStrategy(starting_epsilon_value=0.1, exploration_part=0.7),
                     discount=1),
          DQNAgent(step_size=0.01,
                   discount=1,
                   epsilon_strategy=DecayingSinusEpsilonStrategy(starting_epsilon_value=0.1, exploration_part=0.7),
                   fit_period=64,
                   batch_size=64,
                   max_memory_size=64)]
```
Agents can be manually saved to files:
```python
agent_0_file_path = os.path.join(ABS_PROJECT_ROOT_PATH, "reinforcement_learning", "common", "trained_agents", "agent0.rl_agent")
agent_1_file_path = os.path.join(ABS_PROJECT_ROOT_PATH, "reinforcement_learning", "common", "trained_agents", "agent1.rl_agent")
agents_file_paths = [agent_0_file_path, agent_1_file_path]

[agent.save(agent_file_path) for (agent, agent_file_path) in zip(agents, agents_file_paths)]
```
...and can be loaded from files:
```python
agents = [BaseAgent.load(agent_file_path) for agent_file_path in agents_file_paths]
```

You can also save them to the agents database:

Firstly call AgentsDB.setup() if you want to work on the new agents database
```python
AgentsDB.setup()
```

Secondly save your agents in database
```python
[AgentsDB.save(agent=agents[i],
               player=i,
               board_size=3,
               marks_required=3,
               description="Non-trained agent") for i in range(len(agents))]
```
Here is how agents can be loaded from agents database:
AgentsDB.load method can take subset of these parameters (no parameters is also allowed):
- id : int
- class_name : str
- player : int
- board_size : int
- marks_required : int
- description : str
- agent : BaseAgent
- savetime : Datetime
- And it returns a list of agents objects that satisfy given parameters
```python
agent0 = AgentsDB.load(class_name="NStepAgent", player=0)[0]
agent1 = AgentsDB.load(class_name="DQNAgent", player=1)[0]
agents = [agent0, agent1]
```

Database can be reset with AgentsDB.reset()
```python
AgentsDB.reset()
```

For more sophisticated use of agents database you can use AgentsDB.command method
```python
AgentsDB.command("SELECT * from AGENTS")
```

You can also connect any other db client (e.g. DataGrip) to the agents database

Training is as simple as this:
```python
episodes_no = 1000
with SimpleTraining(engine=engine, agents=agents) as st:
    # assignment is necessary, because training doesn't modify agents provided in constructor
    agents = st.train(episodes_no=episodes_no,
                      auto_saving=100,
                      saving_description=["Trained agent", "Trained agent"])
```
SimpleTraining train method parameters description
- episodes_no: number of episodes to play
- auto_saving:
if None or False-> nothing is saved:
  - if True -> All agents are saved at the and of the training
  - if Integer -> All agents are saved every auto_saving episodes
- saving_description:
  - if None -> All agents are saved with the same standard description: "{episodes_no} episodes"
  - if string -> This string is used as description for saving for all agents
  - if list(string) -> Each agent is saved with his own description from list

Agents can be visualized
```python
[agent.visualize() for agent in agents]
```

### Start a player vs bot TicTacToe game
Make sure that you have following configuration of traing platform config.ini:
```ini
[TRAINING PLATFORM PARAMETERS]
actorsystembase = simpleSystemBase
logging = 0
```
For now, an opponent is loaded as last agent that satisfy mark, board size and marks required.
If you want load specific agent from database in TicTacToeComponent in ```# Oponnent joing``` section change
```python
matching_agents = AgentsDB.load(player=self._opponent_mark,
                                        board_size=self._board_size,
                                        marks_required=self.marks_required)  # List of all agents that satisfy criteria

        # TODO: Make convenient select agent function (maybe in GUI)
        # For now it's just last agent
        def agent_select(agents):
            if not agents:
                raise ValueError("There are now agents satisfying given criteria in the Agents Database")
            return agents[-1]
        agent = agent_select(matching_agents)
```
to
```python
matching_agents = AgentsDB.load(arbitral_subset_of_criterias)
def agent_select(agents):
  if not agents:
      raise ValueError("There are now agents satisfying given criteria in the Agents Database")
  # Some your agent choosing implementation
agent = agent_select(matching_agents)
```
or if you whant use more sophisticated sql query
```python
rows = AgentsDB.command(sql_query_string)
def some_rows_postprocessing(rows):
  # Some your implementation of rows postprocessing
agent = some_rows_postprocessing(rows)
```

Another way is to load agent from file:
```python
agent = BaseAgent.load(agent_file_path)
```

To start a game run launch_application.py typing in console started in project root:
```bash
python game_app/launch_application.py
```

