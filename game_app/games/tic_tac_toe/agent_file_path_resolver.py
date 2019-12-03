# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os
REL_PROJECT_ROOT_PATH = "./../../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#


def resolve_agent_file_path(agents_mark, board_size, marks_required):
    if agents_mark == 0:
        agent_file_name = f"first_player_q_ep_0.ai"
    elif agents_mark == 1:
        agent_file_name = f"second_player_q_ep_0.ai"
    else:
        raise Exception("Invalid opponent mark")

    return os.path.join(ABS_PROJECT_ROOT_PATH, "reinforcement_learning", "agents", agent_file_name)
