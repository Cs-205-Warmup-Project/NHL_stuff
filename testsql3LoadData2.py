import sqlite3
from sqlite3 import Error
import csv

#ToDo Find a permanent way to remove the invisible characters ï»¿ from the beggening the player_info

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

    #Testing to see if the insert method works.
    #iterate through csv file add intormation to dictionary then to column datastructure
    with open('game_goalie_stats.csv', newline='') as goalie_stats_csv:
        goalie_stats_dict = csv.DictReader(goalie_stats_csv)
        goalie_stats_colm = [(i['player_id'], i['team_id'], i['time_on_ice'], i['assists'], i['goals'], i['shots'], i['saves']) for i in goalie_stats_dict]

#Below code gives an error, working it it currently

    with open('GameSkaterStats.csv', newline='') as game_skater_csv:
        game_skater_dict = csv.DictReader(game_skater_csv)
        skater_stats_colm = [(i['ï»¿player_id'], i['team_id'], i['time_on_ice'], i['assists'], i['goals'], i['shots'], i['hits']) for i in game_skater_dict]



    with open('PlayerInfo1.csv', newline='') as player_info_csv:
        player_info_dict = csv.DictReader(player_info_csv)
        player_info_colm = [(i['ï»¿player_id'], i['firstName'], i['lastName'], i['primaryPosition']) for i in player_info_dict]
#add column information to the sqlite3 table
    cursor = conn.cursor()
    cursor.executemany("INSERT INTO game_goalie_stats ( player_id, team_id, time_on_ice, assists, goals, shots, saves ) VALUES (?, ?, ?, ?, ?, ?, ?);", goalie_stats_colm)
    cursor.executemany("INSERT INTO game_skater_stats ( player_id, team_id, time_on_ice, assists, goals, shots, hits ) VALUES (?, ?, ?, ?, ?, ?, ?);", skater_stats_colm)
    cursor.executemany("INSERT INTO player_info ( player_id, firstName, lastName, primaryPosition ) VALUES (?, ?, ?, ?);", player_info_colm)

    cursor.execute("SELECT * FROM game_goalie_stats ORDER BY time_on_ice ;")
    print(cursor.fetchall())
    print('\n')
    cursor.execute("SELECT * FROM game_skater_stats ORDER BY time_on_ice ;")
    print(cursor.fetchall())
    print('\n')


    # Dropping the tables
    cursor.execute("DROP TABLE game_goalie_stats")
    cursor.execute("DROP TABLE game_skater_stats")
    cursor.execute("DROP TABLE player_info")


#Now I need to add data to the tables.
if __name__ == "__main__":
    main()