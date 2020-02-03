import sqlite3
import csv

conn = sqlite3.connect('test.db')

#information on openning csv found here
#https://stackoverflow.com/questions/2887878/importing-a-csv-file-into-a-sqlite3-database-table-using-python
#https://docs.python.org/3/library/csv.html

print ("Opened database successfully");

cursor = conn.cursor()
cursor.execute("CREATE TABLE game_goalie_stats (player_id, team_id, time_on_ice, assists, goals, shots, saves);")
cursor.execute("CREATE TABLE game_skater_stats (player_id, team_id, time_on_ice, assists, goals, shots, hits);")
cursor.execute("CREATE TABLE player_info (player_id, firstName, lastName, primaryPosition);")

#iterate through csv file add intormation to dictionary then to column datastructure
with open('game_goalie_stats.csv', newline='') as goalie_stats_csv:
    goalie_stats_dict = csv.DictReader(goalie_stats_csv)
    goalie_stats_colm = [(i['player_id'], i['team_id'], i['time_on_ice'], i['assists'], i['goals'], i['shots'], i['saves']) for i in goalie_stats_dict]

#Below code gives an error, working it it currently

with open('GameSkaterStats.csv', newline ='') as game_skater_csv:
    game_skater_dict = csv.DictReader(game_skater_csv)
    for i in game_skater_dict:
        print(i)
    skater_stats_colm = [(i['player_id'], i['team_id'], i['time_on_ice'], i['assists'], i['goals'], i['shots'], i['hits']) for i in game_skater_dict]

with open('PlayerInfo1.csv', newline = '') as player_info_csv:
    player_info_dict = csv.DictReader(player_info_csv)
    for i in player_info_dict:
        print(i)
    player_info_colm = [(i['player_id'], i['firstName'], i['lastName'], i['primaryPosition']) for i in player_info_dict]


#add column information to the sqlite3 table
cursor.executemany("INSERT INTO game_goalie_stats ( player_id, team_id, time_on_ice, assists, goals, shots, saves ) VALUES (?, ?, ?, ?, ?, ?, ?);", goalie_stats_colm)
cursor.executemany("INSERT INTO game_skater_stats ( player_id, team_id, time_on_ice, assists, goals, shots, hits ) VALUES (?, ?, ?, ?, ?, ?, ?);", skater_stats_colm)
cursor.executemany("INSERT INTO player_info ( player_id, firstName, lastName, primaryPosition ) VALUES (?, ?, ?, ?);", player_info_colm)

conn.commit()
conn.close()