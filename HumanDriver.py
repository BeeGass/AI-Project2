groupName = "Human"
moveNum = 0


def main ():
    board = Board()
    result = PlayGame(board)

def PlayGame(board):
    global moveNum
    while not path.exists(groupName+".go"): #waits until it is the player's move
       pass
    if path.exists("endgame"):
        #end of game
        print("End of game")
        return 0
    else:
        #read opponent's move here
        if path.exists("move_file"):
            f = open("move_file").read()
            lines = f.split()
            row = LetterToNumber(lines[1])
            col = int(lines[2])
            board.placePiece(row, col, -1, 2, moveNum) #makes opponent move
            moveNum += 1
        #make human move here
        getInput(board)
        moveNum += 1
        return PlayGame(board)

#Gets the player input
#board: The current game state
def getInput(board):
    global moveNum
    val = getInput("Enter a row and column to place a stone (i.e. A 6)")
    vals = val.split()
    row = LetterToNumber(vals[0])
    col = int(vals[1])
    success = board.placePiece(row, col, -1, 1, moveNum)
    if not success:
        print("The move you entered was not a legal move")
        getInput(board)
    else:
        f = open("move_file", "w") #open file to write over
        f.write(val) #Write the inputted move
        f.close()

main()