import sqlite3
import csv

conn = sqlite3.connect('test.db')

#information on openning csv found here
#https://stackoverflow.com/questions/2887878/importing-a-csv-file-into-a-sqlite3-database-table-using-python
#https://docs.python.org/3/library/csv.html

print ("Opened database successfully");

cursor = conn.cursor()
#testing query of data
cursor.execute("SELECT * FROM game_goalie_stats ORDER BY time_on_ice ;")
print(cursor.fetchall())

conn.commit()
conn.close()