#BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os
REL_PROJECT_ROOT_PATH = "./../../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
#-------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

import signal
from parse import parse
from thespian.actors import *

from training_platform.server.common import *
from training_platform.clients.basic_player_clients.terminal_human_player_agent import HumanPlayerAgent
from training_platform.server.service import GameManager, MatchMaker
from training_platform.server.logger import Logger
from environments.tic_tac_toe.tic_tac_toe_engine_utils import Player

def signal_handler(sig, frame):
    asys.tell(match_maker_addr, DetachMsg())
    print('\nDetached from server')
    sys.exit(0)

def log(text):
    asys.tell(logger_addr, LogMsg(text, f"client:{player}"))

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)

    # Commandline parameters parsing
    argc = len(sys.argv)
    if not argc == 3:
        print(f"Invalid arguments number: {argc-1} (should be 2)")
        print("Try again with following arguments:")
        print("python player_client.py <player_name> <player_mark>")
        exit()
    player_name = sys.argv[1]
    player_mark = int(sys.argv[2])

    # Initialization
    player = Player(player_name, player_mark)
    agent = HumanPlayerAgent()
    asys = ActorSystem('multiprocTCPBase')
    match_maker_addr = asys.createActor(MatchMaker, globalName="MatchMaker")
    game_manager_addr = asys.createActor(GameManager, globalName="GameManager")
    logger_addr = asys.createActor(Logger, globalName="Logger")

    # Server joining
    asys.tell(match_maker_addr, JoinMsg(player))
    log("Attempt of server joining")

    # Messages dispatcher
    while True:
        msg = asys.listen()
        if isinstance(msg, YourTurnMsg):
            asys.tell(game_manager_addr, TakeActionMsg(agent.take_action(msg.state, msg.action_space)))
            print("Waiting for your turn...")

        elif isinstance(msg, RewardMsg):
            agent.receive_reward(msg.reward)

        elif isinstance(msg, GameOverMsg):
            agent.exit(msg.state)
            exit()

        elif isinstance(msg, ServiceUninitializedMsg):
            log("Attempt of using not launched service")
            _ = input("Service hasn't been launched yet. Launch service and then press Enter...")
            asys.tell(match_maker_addr, JoinMsg(player))

        elif isinstance(msg, InvalidPlayerMsg):
            log("Invalid player received during joining client handling")
            print("Invalid player received during joining client handling, try one of below:")

            for i in range(len(msg.available_or_replaceable_players)):
                print(f"{i}: {msg.available_or_replaceable_players[i]}")

            input_string = input("\nType number of the chosen player: ")
            result = parse("{}", input_string)
            n = int(result[0])
            player = msg.available_or_replaceable_players[n]

            # Server rejoining
            asys.tell(match_maker_addr, JoinMsg(player))

        elif isinstance(msg, JoinAcknowledgementsMsg):
            log("Succesfully joined server!")
            print("Succesfully joined server!")
            print("Waiting for your turn...")

        elif isinstance(msg, StateUpdateMsg):
            # TODO: StateUpdateMsg handling by clients which don't need it
            pass

