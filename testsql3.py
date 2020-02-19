import sqlite3
import csv

#conn = sqlite3.connect('test.db')

#information on openning csv found here
#https://stackoverflow.com/questions/2887878/importing-a-csv-file-into-a-sqlite3-database-table-using-python
#https://docs.python.org/3/library/csv.html

#print ("Opened database successfully");

#cursor = conn.cursor()
#testing query of data

#cursor.execute("SELECT * FROM game_goalie_stats ORDER BY time_on_ice ;")
#print(cursor.fetchall())
#cursor.execute("SELECT * FROM game_goalie_stats;")
#cursor.execute("SELECT * FROM player_info ;")

#print(cursor.fetchall())

#Create fucntion to take in varables and spit out data
#def retrieveDataFirstLast(firstName, lastName, keyWord):
    #for test purpose
    #value = 31
    #cursor.execute("SELECT player_id FROM game_goalie_stats WHERE " + keyWord + "=?;",(value,))
    #search for player id
#    print(lastName)
    #cursor.execute("SELECT * FROM player_info WHERE lastName=?;", (lastName,))
#    cursor.execute("SELECT * FROM player_info;")
    #search for keyWord data based on player_id
#    print(cursor.fetchall())

# Def of queryDatabaeListMyTeamates
# takes a firstName and lastName
# first step is to get the player_id associated with firstName lastName,
# then we find if that player is in the GameSkaterStats or the game_goalie_stats
# finally returns an array of tuples of the teammates associated with the player_id of firstName lastName.

def queryDatabaseListMyTeamMates(firstName, lastName):
    #database connection
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    print("Searching database for team of " + firstName + " " + lastName)
    #error handleing cases need to go around this..
    cursor.execute("SELECT player_id FROM player_info WHERE  firstName=? AND lastName=?;", (firstName, lastName))
    playerIdArray = cursor.fetchall()
    if (playerIdArray == []):
        print(firstName + " " + lastName + " not found in database")
        #close database connection
        conn.commit()
        conn.close()
        return
    playerId = playerIdArray[0][0]

    #get team id for player
    cursor.execute("SELECT team_id FROM game_skater_stats WHERE  player_id=?;", (playerId,))
    teamIdArray = cursor.fetchall()
    if (teamIdArray == []):
        #print("Not found in game skater stats")
        cursor.execute("SELECT team_id FROM game_goalie_stats WHERE  player_id=?;", (playerId,))
        teamIdArray = cursor.fetchall()
        if (teamIdArray == []):
            print("Team id not found contact developer for support")
            #close database connection
            conn.commit()
            conn.close()
            return
        teamId = teamIdArray[0][0]

    #get all other player ids with that team id
    cursor.execute("SELECT player_id FROM game_goalie_stats WHERE  team_id=?;", (teamId,))
    playerIdTeamArray = cursor.fetchall()

    #print all the names with the set of player ids, in a array of tuples [(first, last), (first, last)...]
    nameListTuples = []
    for playerID in playerIdTeamArray:
        cursor.execute("SELECT firstName, lastName FROM player_info WHERE player_id=?;", playerID)
        firstLast = cursor.fetchall()
        nameListTuples.append(firstLast[0])
        
    #remove duplicates by sending it through a set
    nameListTuples = list(set(nameListTuples))
    #close database connection
    conn.commit()
    conn.close()
    return nameListTuples

# The is empty method tests to see if the parameter structure is empty. Created to test if the player_id tuple is empty.
# Sourced from: https://www.tutorialspoint.com/python_data_access/python_sqlite_drop_table.htm
def is_empty(any_structure):
    if any_structure:
        return False
    else:
        return True

# Def queryKeyword(keyword, firstName, lastName):
# The retirveDataFirstLast method takes a firstName, lastName and a keyword
# The first step is to find the player id where firstName = firstName and lastName = lastName
# Then we need to check and see if that players id is found in the GameSkaterStats.csv or game_goalie_stats.csv
# Once we know the location of the playerId we can then query as follows
# Select keyWord from [table_name] where firstname = firstName and lastname = lastName
def retrieveDataFirstLast(firstName, lastName, keyWord):
    #database connection
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()

    #Checking to see if the player is found in the database
    cursor.execute("SELECT player_id from player_info WHERE firstName=? AND lastName =?", (firstName, lastName))
    player_id = cursor.fetchall()
    if(is_empty(player_id)):
        player_id = '1'
    try:
        cursor.execute("SELECT " + keyWord + " from game_goalie_stats WHERE player_id=?",(player_id[0][0],))
        goalieStats = cursor.fetchall()
        if (goalieStats == []):
            cursor.execute("SELECT " + keyWord + " from game_skater_stats WHERE player_id=?",(player_id[0][0],))
            skaterStats = cursor.fetchall()
            if (skaterStats == []):
                print("No data exists for that query\n")
                #close database connection
                conn.commit()
                conn.close()
                return []
            skaterStats = cursor.fetchall()
            skaterStats = skaterStats[0][0]
            #close database connection
            conn.commit()
            conn.close()
            return skaterStats
        goalieStats = goalieStats[0][0]
        #close database connection
        conn.commit()
        conn.close()
        return goalieStats
    except sqlite3.Error:
        #close database connection
        conn.commit()
        conn.close()
        print("No data exists for that query\n")

#
def queryDatabaseMyTeamName(firstName, lastName):
    #database connection
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    
    #Checking to see if the player is found in the database
    cursor.execute("SELECT player_id from player_info WHERE firstName=? AND lastName =?", (firstName, lastName))
    player_id = cursor.fetchall()
    if(is_empty(player_id)):
        player_id = '1'
    try:
        cursor.execute("SELECT team_id from game_goalie_stats WHERE player_id=?", (player_id[0][0],))
        team = cursor.fetchall()
        if (team == []):
            cursor.execute("SELECT team_id from game_skater_stats WHERE player_id=?", (player_id[0][0],))
            team = cursor.fetchall()
            if (team == []):
                #close database connection
                conn.commit()
                conn.close()
                return ''
            teamName = ''
            if (team[0][0] == '1'):
                teamName = "New Jersey Devils"
            elif (team[0][0] == '4'):
                teamName = "Philadelphia Flyers"
            elif (team[0][0] == '26'):
                teamName = "Los Angeles King"
            elif (team[0][0] == '6'):
                teamName = "Boston Bruins"
            #close database connection
            conn.commit()
            conn.close()
            return teamName
        else:
            teamName = ''
            if(team[0][0] == '1'):
                teamName = "New Jersey Devils"
            elif(team[0][0] == '4'):
                teamName = "Philadelphia Flyers"
            elif(team[0][0] == '26'):
                teamName = "Los Angeles King"
            elif(team[0][0] == '6'):
                teamName = "Boston Bruins"
            #close database connection
            conn.commit()
            conn.close()
            return teamName
            
            #print("Team of " + firstName + " " + lastName + " is " + teamName)
    except sqlite3.Error:
        #close database connection
        conn.commit()
        conn.close()
        return ''
 
#retrieveDataFirstLast("test2", "Timonen", "saves")
names = queryDatabaseListMyTeamMates("Martin", "Jones")
print(names)
names = queryDatabaseListMyTeamMates("sadflk", "saldkfj")
print(names)
#need to think about when stats for goalie only given to stat for skater...
Stats = retrieveDataFirstLast("Martin", "Jones", "shots")
print(Stats)
Stats = retrieveDataFirstLast("Martin", "Jones", "shot")
print(Stats)
team = queryDatabaseMyTeamName("Martin","Brodeur")
print(team)
#conn.commit()
#conn.close()