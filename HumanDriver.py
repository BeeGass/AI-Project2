from os import path
groupName = "Human"

def main ():
    PlayGame()

def PlayGame():
    #exit(0)
    print("Waiting for other player. . .")
    while not path.exists(groupName+".go"): #waits until it is the player's move
       pass
    if path.exists("end_game"):
        #end of game
        print("Game over!")
    else:
        getInput()
        PlayGame()

#Gets the player input
def getInput():
    val = input("Enter a row and column to place a stone (i.e. A 6)")
    strToWrite = groupName + " " + val
    f = open("move_file", "w") #open file to write over
    f.write(strToWrite) #write the inputted move
    f.close()

main()