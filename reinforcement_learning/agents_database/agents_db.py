# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys
import os

REL_PROJECT_ROOT_PATH = "./../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

import sqlite3
import pickle
import datetime


class AgentsDB:
    database_path = os.path.join(ABS_PROJECT_ROOT_PATH, "reinforcement_learning", "db.sqlite")
    conn = sqlite3.connect(database_path)
    cur = conn.cursor()
    create_agents_table_command = """
    CREATE TABLE agents (
        id INTEGER,
        class TEXT,
        player INTEGER,
        board_size INTEGER,
        marks_required INTEGER,
        description TEXT,
        agent BLOB,
        savetime timestamp,
        PRIMARY KEY (id));
    """

    insert_agent_command = """
    INSERT INTO agents (class, player, board_size, marks_required, description, agent, savetime) VALUES (?, ?, ?, ?, ?, ?, ?)
    """

    @staticmethod
    def setup():
        AgentsDB.cur.executescript("DROP TABLE IF EXISTS agents")
        AgentsDB.cur.executescript(AgentsDB.create_agents_table_command)
        AgentsDB.conn.commit()

    @staticmethod
    def save(agent, **kwargs):
        class_name = agent.__class__.__name__.split(".")[-1]
        agent = pickle.dumps(agent)
        player = kwargs.get("player", None)
        board_size = kwargs.get("board_size", None)
        marks_required = kwargs.get("marks_required", None)
        description = kwargs.get("description", None)
        savetime = datetime.datetime.now()

        AgentsDB.cur.execute(AgentsDB.insert_agent_command,
                             (class_name, player, board_size, marks_required, description, agent, savetime))
        AgentsDB.conn.commit()

    @staticmethod
    def load(id):
        AgentsDB.cur.execute("SELECT * FROM agents WHERE id = ?", (id,))
        return pickle.loads(AgentsDB.cur.fetchone()[6])
