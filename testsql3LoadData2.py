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
# keyword, firstName, lastName
#def queryKeyword(keyword, firstName, lastName):


def main():
#
#     database = "test.db"
#
#     sql_create_player_info_table = """ CREATE TABLE IF NOT EXISTS playerInfo (
#                                   player_id integer,
#                                   firstName text,
#                                   lastName text,
#                                   primaryPosition text
#                                   );"""
#     sql_create_game_goalie_table = """ CREATE TABLE IF NOT EXISTS gameGoalie (
#                                         team_id integer,
#                                         player_id,
#                                         time_on_ice integer,
#                                         assists integer,
#                                         goals integer,
#                                         shots integer,
#                                         saves integer
#                                         );"""
#
#     sql_create_game_skater_table = """ CREATE TABLE IF NOT EXISTS gameSkater (
#                                         team_id integer,
#                                         player_id,
#                                         time_on_ice integer,
#                                         assists integer,
#                                         goals integer ,
#                                         shots integer,
#                                         hits integer
#                                         );"""
#     conn = createConnection(database)
#
#     if conn is not None:
#         create_table(conn, sql_create_player_info_table)
#         create_table(conn, sql_create_game_goalie_table)
#         create_table(conn, sql_create_game_skater_table)
#     else:
#         print("Error, cannot create tables")
#
#     #Testing to see if the insert method works.
#     #iterate through csv file add intormation to dictionary then to column datastructure
#     with open('game_goalie_stats.csv', newline='', encoding='utf-8-sig') as goalie_stats_csv:
#         goalie_stats_dict = csv.DictReader(goalie_stats_csv)
#         goalie_stats_colm = [(i['player_id'], i['team_id'], i['time_on_ice'], i['assists'], i['goals'], i['shots'], i['saves']) for i in goalie_stats_dict]
#     goalie_stats_csv.close()
# #Below code gives an error, working it it currently
#
#     with open('GameSkaterStats.csv', newline='', encoding='utf-8-sig') as game_skater_csv:
#         game_skater_dict = csv.DictReader(game_skater_csv)
#         skater_stats_colm = [(i['player_id'], i['team_id'], i['time_on_ice'], i['assists'], i['goals'], i['shots'], i['hits']) for i in game_skater_dict]
#     game_skater_csv.close()
#
#
#     with open('PlayerInfo1.csv', newline='', encoding='utf-8-sig') as player_info_csv:
#         player_info_dict = csv.DictReader(player_info_csv)
#         player_info_colm = [(i['player_id'], i['firstName'], i['lastName'], i['primaryPosition']) for i in player_info_dict]
#     player_info_csv.close()
#     #add column information to the sqlite3 table
#     cursor = conn.cursor()
#     cursor.executemany("INSERT INTO playerInfo ( player_id, firstName, lastName, primaryPosition ) VALUES (?, ?, ?, ?);", player_info_colm)
#     cursor.executemany("INSERT INTO gameGoalie( player_id, team_id, time_on_ice, assists, goals, shots, saves) VALUES (?, ?, ?, ?, ?, ?, ?);", goalie_stats_colm)
#     cursor.executemany("INSERT INTO gameSkater ( player_id, team_id, time_on_ice, assists, goals, shots, hits) VALUES (?, ?, ?, ?, ?, ?, ?);", skater_stats_colm)
#
#     cursor.execute("SELECT * FROM game_goalie_stats ORDER BY time_on_ice ;")
#     print(cursor.fetchall())
#     print('\n')
#     cursor.execute("SELECT * FROM game_skater_stats ORDER BY time_on_ice ;")
#     print(cursor.fetchall())
#     print('\n')
#
#
#     # Dropping the tables
#     cursor.execute("DROP TABLE gameGoalie")
#     cursor.execute("DROP TABLE gameSkater")
#     cursor.execute("DROP TABLE playerInfo")


    conn = sqlite3.connect('test.db')

    # information on openning csv found here
    # https://stackoverflow.com/questions/2887878/importing-a-csv-file-into-a-sqlite3-database-table-using-python
    # https://docs.python.org/3/library/csv.html

    print("Opened database successfully");

    cursor = conn.cursor()
    # Creating the table
    cursor.execute("CREATE TABLE game_goalie_stats (player_id, team_id, time_on_ice, assists, goals, shots, saves);")
    cursor.execute("CREATE TABLE game_skater_stats (player_id, team_id, time_on_ice, assists, goals, shots, hits);")
    cursor.execute("CREATE TABLE player_info (player_id, firstName, lastName, primaryPosition);")

    # iterate through csv file add intormation to dictionary then to column datastructure
    with open('game_goalie_stats.csv', newline='', encoding='utf-8') as goalie_stats_csv:
        goalie_stats_dict = csv.DictReader(goalie_stats_csv)
        goalie_stats_colm = [
            (i['player_id'], i['team_id'], i['time_on_ice'], i['assists'], i['goals'], i['shots'], i['saves']) for i in
            goalie_stats_dict]

    goalie_stats_csv.close()
    # Below code gives an error, working it it currently

    # game_skater_dict = csv.DictReader(open("GameSkaterStats.csv"))
    with open('GameSkaterStats.csv', newline='', encoding='utf-8-sig') as game_skater_csv:
        # print(game_skater_csv)
        game_skater_dict = csv.DictReader(game_skater_csv)
        skater_stats_colm = [
            (j['player_id'], j['team_id'], j['time_on_ice'], j['assists'], j['goals'], j['shots'], j['hits']) for j in
            game_skater_dict]
    game_skater_csv.close()

    """used for testing the encoding format of the file + figuring out extra character removal
    with open('GameSkaterStats.csv', newline='', encoding='utf-8-sig', errors='replace') as f:
        reader = csv.reader(f)
        for row in reader:
            print(row[0])
            if (row[0] != "player_id"):
                #game_skater_dict_tmp['player_id'] = row[0]
                print(row)
    """
    # for i in game_skater_dict:
    #        print(i['player_id'])

    with open('PlayerInfo1.csv', newline='', encoding='utf-8-sig') as player_info_csv:
        player_info_dict = csv.DictReader(player_info_csv)
        player_info_colm = [(i['player_id'], i['firstName'], i['lastName'], i['primaryPosition']) for i in player_info_dict]

    # add column information to the sqlite3 table
    #print("final results")
    #print(goalie_stats_colm)
    #print("final results 2")
    #print(skater_stats_colm)
    #print("final results 3")
    #print(player_info_colm)

    cursor.executemany(
        "INSERT INTO game_goalie_stats ( player_id, team_id, time_on_ice, assists, goals, shots, saves ) VALUES (?, ?, ?, ?, ?, ?, ?);",
        goalie_stats_colm)
    cursor.executemany(
        "INSERT INTO game_skater_stats ( player_id, team_id, time_on_ice, assists, goals, shots, hits ) VALUES (?, ?, ?, ?, ?, ?, ?);",
        skater_stats_colm)
    cursor.executemany("INSERT INTO player_info ( player_id, firstName, lastName, primaryPosition ) VALUES (?, ?, ?, ?);",
                       player_info_colm)
    keyword = "assists"
    if(keyword == "assists"):
        cursor.execute("SELECT assists from game_goalie_stats")
        print(cursor.fetchall())
    elif(keyword == "timeOnIce"):
        cursor.execute("SELECT ")
    elif(keyword == "shots"):
        cursor.execute("SELECT ")
    elif(keyword == "saves"):
        cursor.execute("SELECT ")
    elif(keyword == "goals"):
        cursor.execute("SELECT ")
    elif(keyword == "hits"):
        cursor.execute("SELECT ")
    elif(keyword == "saves"):
        print("NUll")


# Dropping the tables
    cursor.execute("DROP TABLE game_goalie_stats")
    cursor.execute("DROP TABLE game_skater_stats")
    cursor.execute("DROP TABLE player_info")


#Now I need to add data to the tables.
if __name__ == "__main__":
    main()