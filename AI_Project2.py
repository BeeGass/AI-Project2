import os.path
from os import path
groupName = "Sigmoid"

def main():
    boardSize = 15
    
    playGame(board)

#Function which will play the Gomoku game until completion
#board: An array represetnation of the game board
def playGame(board):
    while not path.exists(groupName+".go"): #waits until it is the player's move
       pass
    if path.exists("endgame"):
        #end of game
        print("End of game")
    else:
        #read opponent's move here
        #make move here
        playGame(board) #repeats until game completion

main() #Starts up the main function