from common import *
from human_player_agent import HumanPlayerAgent
from service import GameManager, MatchMaker
import signal
import sys
from logger import Logger
from parse import parse

def signal_handler(sig, frame):
        asys.tell(match_maker_addr, DetachMsg())
        print('\nDetached from server')
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def log(text):
    asys.tell(logger_addr, LogMsg(text, f"client:{player}"))

if __name__ == '__main__':
    # Commandline parameters parsing
    argc = len(sys.argv)
    if not argc == 3:
        print(f"Invalid arguments number: {argc-1} (should be 2)")
        print("Try again with following arguments:")
        print("python client.py <player_name> <player_mark>")
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
    while(True):
        msg = asys.listen()
        if isinstance(msg, YourTurnMsg):
            asys.tell(game_manager_addr, MakeMoveMsg(agent.step(msg.state, msg.allowed_actions)))

        elif isinstance(msg, RewardMsg):
            agent.reward(msg.reward)

        elif isinstance(msg, GameOverMsg):
            agent.exit(msg.state)
            exit()

        elif isinstance(msg, ServiceNotLaunchedMsg):
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

