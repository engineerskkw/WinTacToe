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
    database_path = os.path.join(ABS_PROJECT_ROOT_PATH, "reinforcement_learning", "agents_database", "agents_db.sqlite")
    conn = sqlite3.connect(database_path)
    cur = conn.cursor()
    create_agents_table_command = """
    CREATE TABLE agents (
        id INTEGER,
        class_name TEXT,
        player INTEGER,
        board_size INTEGER,
        marks_required INTEGER,
        description TEXT,
        agent BLOB,
        savetime timestamp,
        PRIMARY KEY (id));
    """

    insert_agent_command = """
    INSERT INTO agents (class_name, player, board_size, marks_required, description, agent, savetime) VALUES (?, ?, ?, ?, ?, ?, ?)
    """

    @staticmethod
    def setup():
        AgentsDB.cur.executescript("DROP TABLE IF EXISTS agents")
        AgentsDB.cur.executescript(AgentsDB.create_agents_table_command)
        AgentsDB.conn.commit()

    @staticmethod
    def save(agent, player, board_size, marks_required, description=""):
        class_name = agent.__class__.__name__.split(".")[-1]
        agent = pickle.dumps(agent)
        savetime = datetime.datetime.now()

        AgentsDB.cur.execute(AgentsDB.insert_agent_command,
                             (class_name, player, board_size, marks_required, description, agent, savetime))
        AgentsDB.conn.commit()

    @staticmethod
    def load(**kwargs):
        parameters = []
        if not kwargs.items():
            query_command = "SELECT * FROM agents"
        else:
            wheres_list = ""

            for column_name, value in kwargs.items():
                wheres_list += f" {column_name} = ?"
                parameters.append(value)
            query_command = f"SELECT * FROM agents WHERE{wheres_list}"
        parameters = tuple(parameters)
        print(query_command)
        print(parameters)
        AgentsDB.cur.execute(query_command, parameters)
        rows = AgentsDB.cur.fetchall()
        print(rows)
        return [pickle.loads(row[6]) for row in rows]

    @staticmethod
    def query(query_command):
        AgentsDB.cur.execute(query_command)
        return AgentsDB.cur.fetchall()
