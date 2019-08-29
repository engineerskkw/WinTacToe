# WinTacToe
WinTacToe is system for training reinforcement learning agents to play tic-tac-toe-related games.
It consist of the following elements:
* Multiple, diverse game environments (compatibile with OpenAI Gym)
* RL agents of various architectures and levels of advancement
* Human player interface which allow to play game with chosen agent(s)

Futhermore WinTacToe allow to analyse agents, including blackbox analysis of neural-networks-based agents

### Installation and launching basic experimental RL Agent jupyter notebook
1. Clone this project:
```console
git clone https://github.com/engineerskkw/WinTacToe.git
```
2. In project's root run (without this flag it fails):
```console
cd WinTacToe/
pipenv install --skip-lock
```
3. Launch project's shell:
```console
pipenv shell
```
4. Launch jupyter notebook:
```console
jupyter notebook
```
[![asciicast](https://asciinema.org/a/xMSq7zpXbkEEgJmrNl3u2cHs0.svg)](https://asciinema.org/a/xMSq7zpXbkEEgJmrNl3u2cHs0)

5. In jupyter navigate to:
```
WinTacToe/src/agents/
```
and open file:
```
Monte_Carlo_agent_alpha_draft.Rmd:
```

6.1 If there are import problems or notebook is ineditable run this command in console:
```console
python -m ipykernel install --user --name=Python3.7-WinTacToe
```

6.2 and change kernel to:
```
Python3.7-WinTacToe
```
### Using
Run all cells in opened jupyter notebook to load all necessary classes and to train an agent.
Display agent's last_episode, returns, policy, action_value, model and MDP to analyse it's behaviour.
Try various values of i.e. epsilon or gamma learning parameters or different board sizes of tic-tac-toe game.
Have fun ;)
