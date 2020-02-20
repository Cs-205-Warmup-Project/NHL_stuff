import sql3Commands
import csv

def main():
    inputString = ""
    possibleKeywords = ["Time On Ice", "Goals", "Assists", "Hits", "Saves", "Primary Position", "Shots"]
    databaseKeywords = ["time_on_ice", "goals", "assists", "hits", "saves", "primaryPosition", "shots"]
    dataLoaded = False
    queryCounter = 0
    while inputString != "Quit":
        inputString = input("Enter query: ")

        # If user inputs "Help", then print out possible keywords
        if inputString == "Help":
            help()
        elif inputString == "Quit":
            break
        # If user inputs "Load Data", then load the data
        elif inputString == "Load Data":
            if(dataLoaded == True):
                print("Database previously loaded, overriding")
            else:
                print("Loading Data")
            dataLoaded = True
            loadData()

        else:
            # Ensure that the data is loaded before completing a query
            if dataLoaded == False:
                print("Data has not been loaded, please enter 'Load Data'")
            else:

                # Split the string into each word
                inputList = inputString.split()

                # Determine where the word "Player" is in the input string
                playerIndex = -1
                for i in range(0, len(inputList)):
                    if inputList[i] == "Player":
                        playerIndex = i
                        break

                # If playerIndex was not updated in loop above, then there was invalid syntax
                if playerIndex == -1:
                    print("Invalid Syntax - no keyword 'Player'")

                # If the word "Player" is exists, then handle the query
                else:
                    # Determine the keyword
                    keyword = ""
                    for i in range(0, playerIndex):
                        keyword += inputList[i] + " "

                    keyword = keyword[0: len(keyword) - 1]

                    # Handle database keyword queries
                    invalidKeyword = True
                    #for possibleKeyword in possibleKeywords:
                    for i in range(len(possibleKeywords)):
                        if keyword == possibleKeywords[i]:
                            dbKeyword = databaseKeywords[i]
                            invalidKeyword = False
                            if (queryCounter == 0):
                                # Open the connection
                                conn = sql3Commands.sqlite3.connect('test.db')
                            queryCounter += 1
                            if len(inputList) == playerIndex + 3:
                                firstName = inputList[playerIndex + 1]
                                lastName = inputList[playerIndex + 2]
                                queryDatabaseKeyword(dbKeyword, keyword, firstName, lastName, conn)
                            else:
                                print("Invalid Syntax - need player's full name")

                    # Handle List My Team keyword queries
                    if keyword == "List My Team":
                        invalidKeyword = False
                        if(queryCounter == 0):
                            #Open the connection
                            conn = sql3Commands.sqlite3.connect('test.db')
                        queryCounter += 1
                        if len(inputList) == playerIndex + 3:
                            firstName = inputList[playerIndex + 1]
                            lastName = inputList[playerIndex + 2]
                            queryDatabaseListMyTeam(firstName, lastName, conn)
                        else:
                            print("Invalid Syntax - need player's full name")

                    # Handle Teammates keyword queries
                    if keyword == "Teammates":
                        invalidKeyword = False
                        if(queryCounter == 0):
                            #Open the connection
                            conn = sql3Commands.sqlite3.connect('test.db')
                        queryCounter += 1

                        if len(inputList) == playerIndex + 3:
                            firstName = inputList[playerIndex + 1]
                            lastName = inputList[playerIndex + 2]
                            queryDatabaseTeammates(firstName, lastName, conn)
                        else:
                            print("Invalid Syntax - need player's full name")


                    # Handle if the keyword is invalid
                    if invalidKeyword:
                        print("Invalid Syntax - '" + keyword + "' is an invalid keyword")


def help():
    print("Possible keywords:")
    print("  'Time On Ice'")
    print("  'Goals'")
    print("  'Assists'")
    print("  'Shots'")
    print("  'Hits'")
    print("  'Saves'")
    print("  'Teammates'")
    print("  'List My Team'")
    print("")
    print("Example query:")
    print("  'Goals Player Zach Parise' -- This will retrieve the total number of goals scored by the player with the name Zach Parise")
    print("")
    print("Example query:")
    print("  'List My Team Player Zach Parise' -- This will retrieve the team Zach Parise plays on")
    print("")
    print("Example query:")
    print("  'Teammates Player Zach Parise' -- This will retrieve all the teammats of Zach Parise in the database")
    print("")
    print("Or enter 'Quit' to exit")



def loadData():
    #print("Loading data")
    conn = sql3Commands.sqlite3.connect('test.db')
    cursor = conn.cursor()

    cursor.execute("DROP TABLE game_goalie_stats")
    cursor.execute("DROP TABLE game_skater_stats")
    cursor.execute("DROP TABLE player_info")

    cursor.execute("CREATE TABLE player_info (player_id PRIMARY KEY, firstName, lastName, primaryPosition);")
    cursor.execute(
        "CREATE TABLE game_goalie_stats (player_id, team_id, time_on_ice, assists, goals, shots, saves, FOREIGN KEY(player_id) REFERENCES player_info(player_id));")
    cursor.execute(
        "CREATE TABLE game_skater_stats (player_id, team_id, time_on_ice, assists, goals, shots, hits, FOREIGN KEY(player_id) REFERENCES player_info(player_id));")

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
    with open('PlayerInfo1.csv', newline='', encoding='utf-8-sig') as player_info_csv:
        player_info_dict = csv.DictReader(player_info_csv)
        player_info_colm = [(i['player_id'], i['firstName'], i['lastName'], i['primaryPosition']) for i in
                            player_info_dict]
    # Inserting data into the different tables
    cursor.executemany(
        "INSERT INTO game_goalie_stats ( player_id, team_id, time_on_ice, assists, goals, shots, saves ) VALUES (?, ?, ?, ?, ?, ?, ?);",
        goalie_stats_colm)
    cursor.executemany(
        "INSERT INTO game_skater_stats ( player_id, team_id, time_on_ice, assists, goals, shots, hits ) VALUES (?, ?, ?, ?, ?, ?, ?);",
        skater_stats_colm)
    cursor.executemany(
        "INSERT INTO player_info ( player_id, firstName, lastName, primaryPosition ) VALUES (?, ?, ?, ?);",
        player_info_colm)

    conn.commit()
    conn.close()


def queryDatabaseKeyword(dbKeyword, keyword, firstName, lastName, conn):
    #print("Searching database for " + keyword + " from " + firstName + " " + lastName)

    value = sql3Commands.retrieveDataFirstLast(firstName, lastName, dbKeyword, conn)
    if (value == []):
        print(firstName + " " + lastName + "'s " + keyword + " could not be found, please check the name and refer to Help")
    else:
        print(keyword + " = " + str(value))

def queryDatabaseListMyTeam(firstName, lastName, conn):
    #print("Searching database the team of " + firstName + " " + lastName)
    value = sql3Commands.queryDatabaseMyTeamName(firstName, lastName, conn)
    if (value == ""):
        print(firstName + " " +lastName + "'s team could not be found, please check the name and refer to Help")
    else:
        print("Team = " + str(value))


def queryDatabaseTeammates(firstName, lastName, conn):
    #print("Searching database for teammates of " + firstName + " " + lastName)
    value = sql3Commands.queryDatabaseListMyTeamMates(firstName, lastName, conn)
    if (value == []):
        print(
            firstName + " " + lastName + "'s additional teammates could not be found, please check the name and refer to Help")
    else:
        print("Teammates:")
        for name in value:
            print("  " + name[0] + " " + name[1])


main()