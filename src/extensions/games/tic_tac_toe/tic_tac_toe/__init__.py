from gym.envs.registration import register

register(
    id='tictactoe-v0',
    entry_point='tic_tac_toe.envs:TicTacToeBasicEnv',
)