import signal
from parse import parse
from thespian.actors import *

from training_platform.common import *
from training_platform.clients.terminal_human_player.terminal_human_player_agent import HumanPlayerAgent
from training_platform.server.service import GameManager, MatchMaker
from training_platform.server.logger import Logger
from environments.tic_tac_toe.tic_tac_toe_engine_utils import Player

def signal_handler(sig, frame):
    asys.tell(match_maker_addr, DetachMsg())
    print('\nDetached from server')
    sys.exit(0)

def log(text):
    asys.tell(logger_addr, LogMsg(text, f"client:{player}"))
    print(text)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)

    # Commandline parameters parsing
    argc = len(sys.argv)
    if not argc == 3:
        print(f"Invalid arguments number: {argc-1} (should be 2)")
        print("Try again with following arguments:")
        print("python agent_client.py <player_name> <player_mark>")
        exit()
    player_name = sys.argv[1]
    player_mark = int(sys.argv[2])

    # Initialization
    player = Player(player_name, player_mark)
    agent = HumanPlayerAgent()
    asys = ActorSystem(ACTOR_SYSTEM_BASE)
    match_maker_addr = asys.createActor(MatchMaker, globalName="MatchMaker")
    game_manager_addr = asys.createActor(GameManager, globalName="GameManager")
    logger_addr = asys.createActor(Logger, globalName="Logger")

    # EnvironmentServer joining
    asys.tell(match_maker_addr, JoinMsg(player, gui_client=True))
    log("Attempt of server joining")

    # Messages dispatcher
    while True:
        msg = asys.listen()
        # Joining messages
        if isinstance(msg, MatchMakerUninitializedMsg):
            log("Can't join server because MatchMaker hasn't ben initialized")
            exit()
        elif isinstance(msg, InvalidPlayerMsg):
            log("Invalid player sent during joining client handling")
            print("Invalid player sent during joining client handling")
            print("Try one of below:")

            for i in range(len(msg.available_or_replaceable_players)):
                print(f"{i}: {msg.available_or_replaceable_players[i]}")

            input_string = input("\nType number of the chosen player: ")
            result = parse("{}", input_string)
            n = int(result[0])
            player = msg.available_or_replaceable_players[n]

            # EnvironmentServer rejoining
            asys.tell(match_maker_addr, JoinMsg(player))

        elif isinstance(msg, JoinAcknowledgementsMsg):
            log("Succesfully joined server!")
            print("wait for other players to make a move...")

        # Playing messages
        elif isinstance(msg, YourTurnMsg):
            asys.tell(game_manager_addr, TakeActionMsg(agent.take_action(msg.state, msg.action_space)))
            print("wait for other players to make a move...")

        elif isinstance(msg, GameOverMsg):
            agent.exit(msg.state)
            exit()

        elif isinstance(msg, StateUpdateMsg):
            agent.update(msg.state)
