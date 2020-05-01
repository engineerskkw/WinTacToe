from training_platform import EnvironmentServer
from environments.tic_tac_toe.tic_tac_toe_engine import TicTacToeEngine

if __name__ == '__main__':
    server = EnvironmentServer(TicTacToeEngine(2, 3, 3))

    input("Press ENTER after all players have joined")

    for i in range(100):
        print(f"Game number: {i}")
        server.start()

    server.shutdown()
    print("Training platform has been shutdowned!")