def main():
    inputString = ""
    databaseKeywords = ["Time On Ice", "Goals", "Assists", "Hits", "Saves", "Primary Position"]
    while inputString != "quit":
        inputString = input("Enter query: ")

        dataLoaded = False
        queryCounter = 0

        # If user inputs "help" print out possible keywords
        if inputString == "Help":
            help()
        elif inputString == "Load Data":
            loadData()
            dataLoaded = True
        else:
            # Ensure that the data is loaded before completing a query
            if dataLoaded == False and queryCounter == 0:
                print("Data has not been loaded, please enter 'Load Data'")

            # Split the string into each word
            inputList = inputString.split()
            print(inputList)

            # Determine where the word "Player" is in the input string
            playerIndex = -1
            for i in range(0, len(inputList)):
                if inputList[i] == "Player":
                    playerIndex = i
                    break

            if playerIndex == -1:
                print("Invalid syntax - no keyword 'Player")
                break
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
                for possibleKeyword in databaseKeywords:
                    if keyword == possibleKeyword:
                        invalidKeyword = False
                        queryCounter += 1
                        if len(inputList) == playerIndex + 3:
                            firstName = inputList[playerIndex + 1]
                            lastName = inputList[playerIndex + 2]
                            queryDatabaseKeyword(keyword, firstName, lastName)
                        else:
                            print("Need player's full name")

                # Handle List My Team keyword queries
                if keyword == "List My Team":
                    invalidKeyword = False
                    queryCounter += 1
                    if len(inputList) == playerIndex + 3:
                        firstName = inputList[playerIndex + 1]
                        lastName = inputList[playerIndex + 2]
                        queryDatabaseListMyTeam(firstName, lastName)
                    else:
                        print("Need player's name")

                # Handle Teammates keyword queries
                if keyword == "Teammates":
                    invalidKeyword = False
                    queryCounter += 1
                    names = []
                    playerCount = 0
                    for i in range(0, len(inputList)):
                        if inputList[i] == "Player":
                            playerCount += 1

                    if len(inputList) == (playerCount * 3) + 1:
                        for i in range(playerIndex, len(inputList) - 1, 3):
                            playerTuple = (inputList[i+1], inputList[i+2])
                            names.append(playerTuple)
                            queryDatabaseTeammates(names)
                    else:
                        print("Invalid syntax = need 'Player <first name> <last name>'")

                # Handle if the keyword is invalid
                if invalidKeyword:
                    print(keyword + " is an invalid keyword")


def help():
    print("Possible keywords:")
    print("'Time On Ice'")
    print("'Goals'")
    print("'Assists'")
    print("'Shots'")
    print("'Hits'")
    print("'Saves")
    print("")
    print("Example query:")
    print("Goals Player Wayne Gretzky")
    print("This will retrieve the total number of goals scored by the player with the name Wayne Gretzky")


def loadData():
    print("Loading data")


def queryDatabaseKeyword(keyword, firstName, lastName):
    print("Searching database for " + keyword + " from " + firstName + " " + lastName)


def queryDatabaseListMyTeam(firstName, lastName):
    print("Searching database the team of " + firstName + " " + lastName)


def queryDatabaseTeammates(names):
    print("Searching database for teammates of " + str(names))


main()

