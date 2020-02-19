import sqlite3
from sqlite3 import Error
import csv

# The is empty method tests to see if the parameter structure is empty. Created to test if the player_id tuple is empty.
# Sourced from: https://www.tutorialspoint.com/python_data_access/python_sqlite_drop_table.htm
def is_empty(any_structure):
    if any_structure:
        return False
    else:
        return True

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

# def of queryDatabaseListMyTeam
# takes a firstName and lastName
# first step is to get player_id where firstName = firstName and lastName = lastName.
# Then find which table that player_id is in
# Then get the team_id and return the teamName associated with that team_id
# Return the team that Player firstName lastName is on

def queryDatabaseListMyTeam(firstName, lastName,cursor):
    #Creating lists to know what table player_id's are located in
    goalieId = ["8455710","8468524","8471712","8476234","8468038","8474889"]
    skaterID = ["8467412","8468501","8470609","8471816","8472410","8471233","8470920","8473646","8470610","8472382","8474641",
                "8460626","8472394","8464977","8469454","8469623","8460465","8460542","8468486","8459670","8470640","8473512",
                "8470601","8475640","8470171","8474892","8476177","8448208"]
    #Checking to see if the player is found in the database
    cursor.execute("SELECT player_id from player_info WHERE firstName=? AND lastName =?", (firstName, lastName))
    player_id = cursor.fetchall()
    if(is_empty(player_id)):
        player_id = '1'
    if(goalieId.count(player_id[0][0]) == 0 and skaterID.count(player_id[0][0]) == 0):
        print("That player is not in the database")

    try:
        if(goalieId.count(player_id[0][0]) != 0):
            cursor.execute("SELECT team_id from game_goalie_stats WHERE player_id=?", (player_id[0][0],))
            team = cursor.fetchall()
            teamName = ''
            if(team[0][0] == '1'):
                teamName = "New Jersey Devils"
            elif(team[0][0] == '4'):
                teamName = "Philadelphia Flyers"
            elif(team[0][0] == '26'):
                teamName = "Los Angeles King"
            elif(team[0][0] == '6'):
                teamName = "Boston Bruins"
            print("Team of " + firstName + " " + lastName + " is " + teamName)
        elif(skaterID.count(player_id[0][0] != 0)):
            cursor.execute("SELECT team_id from game_skater_stats WHERE player_id=?", (player_id[0][0],))
            team = cursor.fetchall()
            teamName = ''
            if (team[0][0] == '1'):
                teamName = "New Jersey Devils"
            elif (team[0][0] == '4'):
                teamName = "Philadelphia Flyers"
            elif (team[0][0] == '26'):
                teamName = "Los Angeles King"
            elif (team[0][0] == '6'):
                teamName = "Boston Bruins"
            print("Team of " + firstName + " " + lastName + " is " + teamName)
    except sqlite3.Error:
        print("No data found for that query.\n")


# keyword, firstName, lastName
# def queryKeyword(keyword, firstName, lastName):
# The retirveDataFirstLast method takes a firstName, lastName and a keyword
# The first step is to find the player id where firstName = firstName and lastName = lastName
# Then we need to check and see if that players id is found in the GameSkaterStats.csv or game_goalie_stats.csv
# Once we know the location of the playerId we can then query as follows
# Select keyWord from [table_name] where firstname = firstName and lastname = lastName
def retrieveDataFirstLast(firstName, lastName, keyWord,cursor):
    #Creating lists to know what table player_id's are located in
    goalieId = ["8455710","8468524","8471712","8476234","8468038","8474889"]
    skaterID = ["8467412","8468501","8470609","8471816","8472410","8471233","8470920","8473646","8470610","8472382","8474641",
                "8460626","8472394","8464977","8469454","8469623","8460465","8460542","8468486","8459670","8470640","8473512",
                "8470601","8475640","8470171","8474892","8476177","8448208"]
    #Checking to see if the player is found in the database
    cursor.execute("SELECT player_id from player_info WHERE firstName=? AND lastName =?", (firstName, lastName))
    player_id = cursor.fetchall()
    if(is_empty(player_id)):
        player_id = '1'
    if(goalieId.count(player_id[0][0]) == 0 and skaterID.count(player_id[0][0]) == 0):
        print("That player is not in the database")
    try:
        if (keyWord == "assists"):
            if(goalieId.count(player_id[0][0]) != 0):
                cursor.execute("SELECT assists from game_goalie_stats WHERE player_id=?",(player_id[0][0],))
                print(cursor.fetchall())
            else:
                cursor.execute("SELECT assists from game_skater_stats WHERE player_id=?", (player_id[0][0],))
                print(cursor.fetchall())
        elif (keyWord == "timeOnIce"):
            if (goalieId.count(player_id[0][0]) != 0):
                cursor.execute("SELECT time_on_ice from game_goalie_stats WHERE player_id=?", (player_id[0][0],))
                print(cursor.fetchall())
            else:
                cursor.execute("SELECT time_on_ice from game_skater_stats WHERE player_id=?", (player_id[0][0],))
                print(cursor.fetchall())
        elif (keyWord == "shots"):
            if (goalieId.count(player_id[0][0]) != 0):
                cursor.execute("SELECT shots from game_goalie_stats WHERE player_id=?", (player_id[0][0],))
                print(cursor.fetchall())
            else:
                cursor.execute("SELECT shots from game_skater_stats WHERE player_id=?", (player_id[0][0],))
                print(cursor.fetchall())
        elif (keyWord == "saves"):
            if (goalieId.count(player_id[0][0]) != 0):
                cursor.execute("SELECT saves from game_goalie_stats WHERE player_id=?", (player_id[0][0],))
                print(cursor.fetchall())
            else:
                cursor.execute("SELECT saves from game_skater_stats WHERE player_id=?", (player_id[0][0],))
                print(cursor.fetchall())
        elif (keyWord == "goals"):
            if (goalieId.count(player_id[0][0]) != 0):
                cursor.execute("SELECT goals from game_goalie_stats WHERE player_id=?", (player_id[0][0],))
                print(cursor.fetchall())
            else:
                cursor.execute("SELECT goals from game_skater_stats WHERE player_id=?", (player_id[0][0],))
                print(cursor.fetchall())
        # if the keyWord = hits then we know the player id will be found in the GameSkaterStats.csv
        elif (keyWord == "hits"):
            if (goalieId.count(player_id[0][0]) != 0):
                cursor.execute("SELECT hits from game_goalie_stats WHERE player_id=?", (player_id[0][0],))
                print(cursor.fetchall())
            else:
                cursor.execute("SELECT hits from game_skater_stats WHERE player_id=?", (player_id[0][0],))
                print(cursor.fetchall())
    except sqlite3.Error:
        print("No data exists for that query\n")


def main():
    conn = sqlite3.connect('test.db')
    # information on openning csv found here
    # https://stackoverflow.com/questions/2887878/importing-a-csv-file-into-a-sqlite3-database-table-using-python
    # https://docs.python.org/3/library/csv.html
    cursor = conn.cursor()
    # Creating the table
    cursor.execute("CREATE TABLE player_info (player_id PRIMARY KEY, firstName, lastName, primaryPosition);")
    cursor.execute("CREATE TABLE game_goalie_stats (player_id, team_id, time_on_ice, assists, goals, shots, saves, FOREIGN KEY(player_id) REFERENCES player_info(player_id));")
    cursor.execute("CREATE TABLE game_skater_stats (player_id, team_id, time_on_ice, assists, goals, shots, hits, FOREIGN KEY(player_id) REFERENCES player_info(player_id));")

    # iterate through csv file add intormation to dictionary then to column datastructure
    with open('game_goalie_stats.csv', newline='', encoding='utf-8') as goalie_stats_csv:
        goalie_stats_dict = csv.DictReader(goalie_stats_csv)
        goalie_stats_colm = [
            (i['player_id'], i['team_id'], i['time_on_ice'], i['assists'], i['goals'], i['shots'], i['saves']) for i in
            goalie_stats_dict]
    goalie_stats_csv.close()
    with open('GameSkaterStats.csv', newline='', encoding='utf-8-sig') as game_skater_csv:
        # print(game_skater_csv)
        game_skater_dict = csv.DictReader(game_skater_csv)
        skater_stats_colm = [
            (j['player_id'], j['team_id'], j['time_on_ice'], j['assists'], j['goals'], j['shots'], j['hits']) for j in
            game_skater_dict]
    game_skater_csv.close()
    # Ask what this does
    """used for testing the encoding format of the file + figuring out extra character removal
    with open('GameSkaterStats.csv', newline='', encoding='utf-8-sig', errors='replace') as f:
        reader = csv.reader(f)
        for row in reader:
            print(row[0])
            if (row[0] != "player_id"):
                #game_skater_dict_tmp['player_id'] = row[0]
                print(row)
    """
    with open('PlayerInfo1.csv', newline='', encoding='utf-8-sig') as player_info_csv:
        player_info_dict = csv.DictReader(player_info_csv)
        player_info_colm = [(i['player_id'], i['firstName'], i['lastName'], i['primaryPosition']) for i in player_info_dict]
    # Inserting data into the different tables
    cursor.executemany(
        "INSERT INTO game_goalie_stats ( player_id, team_id, time_on_ice, assists, goals, shots, saves ) VALUES (?, ?, ?, ?, ?, ?, ?);",
        goalie_stats_colm)
    cursor.executemany(
        "INSERT INTO game_skater_stats ( player_id, team_id, time_on_ice, assists, goals, shots, hits ) VALUES (?, ?, ?, ?, ?, ?, ?);",
        skater_stats_colm)
    cursor.executemany("INSERT INTO player_info ( player_id, firstName, lastName, primaryPosition ) VALUES (?, ?, ?, ?);",
                       player_info_colm)
    # Testing my retrieveDataFirstLast method
    retrieveDataFirstLast("Martin","Brodeur","saves",cursor)
    retrieveDataFirstLast("Martin","Brodeur","hits",cursor)
    retrieveDataFirstLast("Martin","Brodeur","saves",cursor)
    retrieveDataFirstLast("Titos","&","soda",cursor)
    queryDatabaseListMyTeam("Martin","Brodeur",cursor)
    queryDatabaseListMyTeam("Martin","B",cursor)


    # Dropping the tables
    # Information on dropping tables: https://www.tutorialspoint.com/python_data_access/python_sqlite_drop_table.htm
    cursor.execute("DROP TABLE game_goalie_stats")
    cursor.execute("DROP TABLE game_skater_stats")
    cursor.execute("DROP TABLE player_info")

    # executing the dropping of the tables. Allows for program to be run repeatedly
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()