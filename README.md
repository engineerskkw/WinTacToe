# WinTacToe
WinTacToe is a system for training **reinforcement learning** agents to play tic-tac-toe-related games.
It consists of the following elements:
* Multiple, diverse game environments
* RL agents of various architectures and levels of advancement
* **Human player interface** which allow to play game with the chosen agent(s)

Futhermore WinTacToe allows to analyse agents, including **blackbox analysis of neural-networks-based agents**

## Beginners guide
### Starting bot vs bot vs ... vs bot training with any engine:
Make sure that you have following configuration of traing platform config.ini:
```
[TRAINING PLATFORM PARAMETERS]
actorsystembase = simpleSystemBase
logging = 0
```

Firstly, you need an engine
```python
engine = TicTacToeEngine(2, 3, 3)
```
Secondly, agents:
```
agents = [BasicAgent(), QLearningAgent(0.3, 0.1, 0.9)]
```

You can also load previously saved agents from files (these paths are examplary):
```python
agent_0_file_path = os.path.join(ABS_PROJECT_ROOT_PATH, "training_platform", "examples", "agent0.ai")
agent_1_file_path = os.path.join(ABS_PROJECT_ROOT_PATH, "training_platform", "examples", "agent1.ai")
agents_file_paths = [agent_0_file_path, agent_1_file_path]
agents = [BaseAgent.load(file_path) for file_path in agents_file_paths]
```

Training is as simple as this:
```python
number_of_episodes = 100
with SimpleTraining(engine, agents) as st:  # using "with statement" is encouraged
    # assignment is necessary, because training doesn't modify agents provided in constructor
    agents = st.train(number_of_episodes)
```

At the end you can save your trained agents
```python
[agent.save(file_path) for (agent, file_path) in zip(agents, agents_file_paths)]
```

### Start a player vs bot game wih any engine
Make sure that you have following configuration of traing platform config.ini:
```
[TRAINING PLATFORM PARAMETERS]
actorsystembase = simpleSystemBase
logging = 0
```
In TicTacToeComponent in ```# Oponnent joing``` section:
```python
# Opponent joining
p1 = players[self._opponent_mark]
c1 = AgentClient(BasicAgent())
self.server.join(c1, p1)
self.log(f"Joined opponent")
```
change ```BasicAgent()``` to ```BaseAgent.load(file_path)```
where ```file_path``` is path to the file containing your saved RL agent.
To start a game run launch_application.py typing in console started in project root:
```
python game_app/launch_application.py
```

# How to stop/start/restart the server and clients (distributed execution) with eny engine
```
TODO
```

# How to start monitor actor
Make sure that you have following configuration of traing platform config.ini:
```
[TRAINING PLATFORM PARAMETERS]
actorsystembase = multiprocTCPBase
logging = 1
```

Firstly start a monitor:
```
python training_platform/examples/start_monitor_client.py
```
Secondly start your training or game player vs bot
