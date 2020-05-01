import os
from global_constants import ABS_PROJECT_ROOT_PATH


def resolve_agent_file_path(agents_mark, board_size, marks_required):
    if agents_mark == 0:
        agent_file_name = f"first_player_q_ep_0.ai"
    elif agents_mark == 1:
        agent_file_name = f"second_player_q_ep_0.ai"
    else:
        raise Exception("Invalid opponent mark")

    return os.path.join(ABS_PROJECT_ROOT_PATH, "test_reinforcement_learning", "agents", agent_file_name)
