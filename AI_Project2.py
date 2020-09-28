import os.path
from os import path
groupName = "Sigmoid"

def main():
    playGame()

def playGame():
    while not path.exists(groupName+".go"): #waits until it is the player's move
       pass
    if path.exists("endgame"):
        #end of game
        print("End of game")
    else:
        #read opponent's move here
        #make move here
        playGame() #repeats until game completion