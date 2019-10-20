from common import *
from human_player_agent import HumanPlayerAgent
from service import GameManager, MatchMaker

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

    # Server joining
    asys.tell(match_maker_addr, JoinMsg(player))

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
