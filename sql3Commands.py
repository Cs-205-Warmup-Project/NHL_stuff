import sqlite3
import csv

def is_empty(any_structure):
    if any_structure:
        return False
    else:
        return True

# def of queryDatabaseListMyTeam
# takes a firstName and lastName
# first step is to get player_id where firstName = firstName and lastName = lastName.
# Then find which table that player_id is in
# Then get the team_id and return the teamName associated with that team_id
# Return the team that Player firstName lastName is on
def queryDatabaseListMyTeamMates(firstName, lastName, conn):
    #database connection
    cursor = conn.cursor()
    #error handleing cases need to go around this..
    cursor.execute("SELECT player_id FROM player_info WHERE  firstName=? AND lastName=?;", (firstName, lastName))
    playerIdArray = cursor.fetchall()
    if (playerIdArray == []):
        #update database connection
        conn.commit()
        return []
    playerId = playerIdArray[0][0]
    #get team id for player
    cursor.execute("SELECT team_id FROM game_skater_stats WHERE  player_id=?;", (playerId,))
    teamIdArray = cursor.fetchall()
    if (teamIdArray == []):
        cursor.execute("SELECT team_id FROM game_goalie_stats WHERE  player_id=?;", (playerId,))
        teamIdArray = cursor.fetchall()
        if (teamIdArray == []):
            #update database connection
            conn.commit()
            return []
    teamId = teamIdArray[0][0]
    #get all other player ids with that team id
    cursor.execute("SELECT player_id FROM game_goalie_stats WHERE team_id=?;", (teamId,))  
    playerIdTeamArray = cursor.fetchall()
    cursor.execute("SELECT player_id FROM game_skater_stats WHERE team_id=?;", (teamId,))
    playerIds = cursor.fetchall()
    playerIdTeamArray = playerIdTeamArray + playerIds
    #return all the names with the set of player ids, in a array of tuples [(first, last), (first, last)...]
    nameListTuples = []
    if (playerIdTeamArray == []):
        return None
    for playerID in playerIdTeamArray:
        #print(playerID[0])
        if (playerID[0] != playerId):
            cursor.execute("SELECT firstName, lastName FROM player_info WHERE player_id=?;", playerID)
            firstLast = cursor.fetchall()
            nameListTuples.append(firstLast[0])
    #remove duplicates by sending it through a set
    nameListTuples = list(set(nameListTuples))
    #update database connection
    conn.commit()
    return nameListTuples

# keyword, firstName, lastName
# def queryKeyword(keyword, firstName, lastName):
# The retirveDataFirstLast method takes a firstName, lastName and a keyword
# The first step is to find the player id where firstName = firstName and lastName = lastName
# Then we need to check and see if that players id is found in the GameSkaterStats.csv or game_goalie_stats.csv
# Once we know the location of the playerId we can then query as follows
# Select keyWord from [table_name] where firstname = firstName and lastname = lastName
def retrieveDataFirstLast(firstName, lastName, keyWord, conn):
    #database connection
    cursor = conn.cursor()
    #Checking to see if the player is found in the database
    cursor.execute("SELECT player_id from player_info WHERE firstName=? AND lastName =?", (firstName, lastName))
    player_id = cursor.fetchall()
    if(is_empty(player_id)):
        player_id = '1'
    try:
        cursor.execute("SELECT " + keyWord + " from game_goalie_stats WHERE player_id=?",(player_id[0][0],))
        goalieStats = cursor.fetchall()
        print(goalieStats)
    except:
        goalieStats = []
    if (goalieStats == []):
        cursor.execute("SELECT " + keyWord + " from game_skater_stats WHERE player_id=?",(player_id[0][0],))
        skaterStats = cursor.fetchall()
        if (skaterStats == []):
            #update database connection
            conn.commit()
            return []
        #iterate through all games to get totals
        total = 0
        for gameStat in skaterStats:
            total = total + int(gameStat[0])
        #update database connection
        conn.commit()
        return total
    total = 0
    for gameStat in goalieStats:
        total = total + int(gameStat[0])
    #update database connection
    conn.commit()
    return total

# def of queryDatabaseListMyTeam
# takes a firstName and lastName
# first step is to get player_id where firstName = firstName and lastName = lastName.
# Then find which table that player_id is in
# Then get the team_id and return the teamName associated with that team_id
# Return the team that Player firstName lastName is on
def queryDatabaseMyTeamName(firstName, lastName, conn):
    #database connection
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
                #update database connection
                conn.commit()
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
            #update database connection
            conn.commit()
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
            #update database connection
            conn.commit()
            return teamName
    except sqlite3.Error:
        #update database connection
        conn.commit()
        return ''