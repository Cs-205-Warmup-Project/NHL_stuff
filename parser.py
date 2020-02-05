def main():
    inputString = ""
    possibleKeywords = ["Time On Ice", "Goals", "Assists", "Hits", "Saves"]
    while(inputString != "quit"):
        inputString = input("Enter query: ")

        # If user inputs "help" print out possible keywords
        if(inputString == "help"):
            help()
        else:
            # Split the string into each word
            inputList = inputString.split()
            #print(inputList)

            # Get the keyword (can be multiple words like Time On Ice
            keyword = ""
            for i in range(0, len(inputList) - 3):
                keyword += inputList[i] + " "
            keyword = keyword[0: len(keyword) - 1]
            #print("'" + keyword + "'")

            # Check if keyword is valid
            validKeyword = False
            for possibleKeyword in possibleKeywords:
                if(keyword == possibleKeyword):
                    validKeyword = True

            # If keyword is invalid, tell user
            if(validKeyword == False):
                print(keyword + " is not a valid keyword")
            else:
                queryDatabaseKeyword(keyword, inputList[len(inputList) - 2], inputList[len(inputList) - 1])

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

def queryDatabaseKeyword(keyword, firstName, lastName):
    print("Searching database for " + keyword + " from " + firstName + " " + lastName)

def queryDatabaseListMyTeam(firstName, lastName):
    print("Searching database for team of " + firstName + " " + lastName)

def queryDatabaseTeammates(names):
    print("Searching database for team of " + names[0][0])


main()