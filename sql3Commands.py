import sqlite3
import csv

def is_empty(any_structure):
    if any_structure:
        return False
    else:
        return True

def queryDatabaseListMyTeamMates(firstName, lastName):
    #database connection
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    #error handleing cases need to go around this..
    cursor.execute("SELECT player_id FROM player_info WHERE  firstName=? AND lastName=?;", (firstName, lastName))
    playerIdArray = cursor.fetchall()
    if (playerIdArray == []):
        #close database connection
        conn.commit()
        conn.close()
        return []
    playerId = playerIdArray[0][0]
    #get team id for player
    cursor.execute("SELECT team_id FROM game_skater_stats WHERE  player_id=?;", (playerId,))
    teamIdArray = cursor.fetchall()
    if (teamIdArray == []):
        cursor.execute("SELECT team_id FROM game_goalie_stats WHERE  player_id=?;", (playerId,))
        teamIdArray = cursor.fetchall()
        if (teamIdArray == []):
            #close database connection
            conn.commit()
            conn.close()
            return []
        teamId = teamIdArray[0][0]

    #get all other player ids with that team id
    cursor.execute("SELECT player_id FROM game_goalie_stats WHERE  team_id=?;", (teamId,))
    playerIdTeamArray = cursor.fetchall()

    #return all the names with the set of player ids, in a array of tuples [(first, last), (first, last)...]
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
            if (skaterStats == []):
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
        return ''
        
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

    except sqlite3.Error:
        #close database connection
        conn.commit()
        conn.close()
        return ''
 
names = queryDatabaseListMyTeamMates("Martin", "Jones")
print(names)
names = queryDatabaseListMyTeamMates("sadflk", "saldkfj")
print(names)
#need to think about when stats for goalie only given to stat for skater...
Stats = retrieveDataFirstLast("Martin", "Jones", "shots")
print(Stats)
Stats = retrieveDataFirstLast("Martin", "Jones", "shotsdf")
print(Stats)
team = queryDatabaseMyTeamName("Martin","Brodeur")
print(team)
team = queryDatabaseMyTeamName("made","up")
print(team)