import sql3Commands

def main():
    inputString = ""
    possibleKeywords = ["Time On Ice", "Goals", "Assists", "Hits", "Saves", "Primary Position", "Shots"]
    databaseKeywords = ["time_on_ice", "goals", "assists", "hits", "saves", "primary_position", "shots"]
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
            dataLoaded = True
            loadData()

        else:
            # Ensure that the data is loaded before completing a query
            if dataLoaded == False:
                print("Data has not been loaded, please enter 'Load Data'")
            else:

                # Split the string into each word
                inputList = inputString.split()
                print(inputList)

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
                    print("keyword = " + keyword)

                    # Handle database keyword queries
                    invalidKeyword = True
                    #for possibleKeyword in possibleKeywords:
                    for i in range(len(possibleKeywords)):
                        if keyword == possibleKeywords[i]:
                            keyword = databaseKeywords[i]
                            invalidKeyword = False
                            if (queryCounter == 0):
                                # Open the connection
                                conn = sql3Commands.sqlite3.connect('test.db')
                            queryCounter += 1
                            if len(inputList) == playerIndex + 3:
                                firstName = inputList[playerIndex + 1]
                                lastName = inputList[playerIndex + 2]
                                queryDatabaseKeyword(keyword, firstName, lastName, conn)
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
    print("'Time On Ice'")
    print("'Goals'")
    print("'Assists'")
    print("'Shots'")
    print("'Hits'")
    print("'Saves")
    print("'Teammates")
    print("'List My Team")
    print("")
    print("Example query:")
    print("Goals Player Wayne Gretzky")
    print("This will retrieve the total number of goals scored by the player with the name Wayne Gretzky")
    print("Example query:")
    print("List My Team Player Wayne Gretzky")
    print("This will retrieve the team Wayne Gretzky plays on")
    print("Example query:")
    print("Teammates Player Wayne Gretzky Player Bob Smith")
    print("This will retrieve whether or not Wayne Gretzky and Bob Smith are Teammates")
    print("")
    print("Or enter 'Quit' to exit")



def loadData():
    print("Loading data")


def queryDatabaseKeyword(keyword, firstName, lastName, conn):
    #print("Searching database for " + keyword + " from " + firstName + " " + lastName)
    value = sql3Commands.retrieveDataFirstLast(firstName, lastName, keyword, conn)
    print(value)

def queryDatabaseListMyTeam(firstName, lastName, conn):
    #print("Searching database the team of " + firstName + " " + lastName)
    value = sql3Commands.queryDatabaseMyTeamName(firstName, lastName, conn)
    print(value)


def queryDatabaseTeammates(firstName, lastName, conn):
    #print("Searching database for teammates of " + firstName + " " + lastName)
    value = sql3Commands.queryDatabaseListMyTeamMates(firstName, lastName, conn)
    for name in value:
        print(name[0] + " " + name[1])


main()