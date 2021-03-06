import sqlite3
import pickle
import datetime
import os


class AgentsDB:
    database_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "agents_db.sqlite")
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

    reset = setup

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

            first = True
            for column_name, value in kwargs.items():
                if not first:
                    wheres_list += " AND"
                else:
                    first = False
                wheres_list += f" {column_name} = ?"
                parameters.append(value)
            query_command = f"SELECT * FROM agents WHERE{wheres_list}"
        parameters = tuple(parameters)
        AgentsDB.cur.execute(query_command, parameters)
        rows = AgentsDB.cur.fetchall()
        return [pickle.loads(row[6]) for row in rows]

    @staticmethod
    def command(query_command):
        AgentsDB.cur.execute(query_command)
        return AgentsDB.cur.fetchall()
