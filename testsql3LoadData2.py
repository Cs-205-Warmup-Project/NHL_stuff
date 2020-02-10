import sqlite3
from sqlite3 import Error
#Creating connection method.
def createConnection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn
def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def main():
    database = "test.db"

    sql_create_player_info_table = """ CREATE TABLE IF NOT EXISTS playerInfo (
                                  player_id integer PRIMARY KEY, 
                                  firstName text NOT NULL,
                                  lastName text NOT NULL,
                                  primaryPosition text NOT NULL
                                  );"""
    sql_create_game_goalie_table = """ CREATE TABLE IF NOT EXISTS gameGoalie (
                                        team_id integer PRIMARY KEY,
                                        player_id REFERENCES playerInfo(player_id),
                                        time_on_ice integer NOT NULL,
                                        assists integer NOT NULL,
                                        goals integer NOT NULL,
                                        shots integer NOT NULL,
                                        saves integer NOT NULL
                                        );"""

    sql_create_game_skater_table = """ CREATE TABLE IF NOT EXISTS gameSkater (
                                        team_id integer PRIMARY KEY,
                                        player_id REFERENCES playerInfo(player_id),
                                        time_on_ice integer NOT NULL,
                                        assists integer NOT NULL,
                                        goals integer NOT NULL,
                                        shots integer NOT NULL,
                                        hits integer NOT NULL
                                        );"""
    conn = createConnection(database)

    if conn is not None:
        create_table(conn, sql_create_player_info_table)
        create_table(conn, sql_create_game_goalie_table)
        create_table(conn, sql_create_game_skater_table)
    else:
        print("Error, cannot create tables")
#Now I need to add data to the tables.
if __name__ == "__main__":
    main()