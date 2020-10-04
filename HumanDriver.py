groupName = "Human"

def main ():
    PlayGame()

def PlayGame(board):
    while not path.exists(groupName+".go"): #waits until it is the player's move
       pass
    if path.exists("endgame"):
        #end of game
        print("End of game")
    else:
        getInput()
        PlayGame()

#Gets the player input
def getInput():
    val = input("Enter a row and column to place a stone (i.e. A 6)")
    vals = val.split()
    row = LetterToNumber(vals[0])
    col = int(vals[1])
    f = open("move_file", "w") #open file to write over
    f.write(val) #write the inputted move
    f.close()

def NumberToLetter(inputColAsNumber):
    theLetter = chr(ord('@') + inputColAsNumber)
    return theLetter

main()