import sqlite3
import csv

conn = sqlite3.connect('test.db')

#information on openning csv found here
#https://stackoverflow.com/questions/2887878/importing-a-csv-file-into-a-sqlite3-database-table-using-python
#https://docs.python.org/3/library/csv.html

print ("Opened database successfully");

cursor = conn.cursor()
cursor.execute("CREATE TABLE game_goalie_stats (player_id, team_id, time_on_ice, assists, goals, shots, saves);")

#iterate through csv file add intormation to dictionary then to column datastructure
with open('game_goalie_stats.csv', newline='') as goalie_stats_csv:
    goalie_stats_dict = csv.DictReader(goalie_stats_csv)
    goalie_stats_colm = [(i['player_id'], i['team_id'], i['time_on_ice'], i['assists'], i['goals'], i['shots'], i['saves']) for i in goalie_stats_dict]

#add column information to the sqlite3 table
cursor.executemany("INSERT INTO game_goalie_stats ( player_id, team_id, time_on_ice, assists, goals, shots, saves ) VALUES (?, ?, ?, ?, ?, ?, ?);", goalie_stats_colm)
conn.commit()
conn.close()