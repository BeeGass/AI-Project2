import os.path
from os import path
groupName = "Sigmoid"

def main():
    playGame()

def playGame():
    while not path.exists(groupName+".txt") #Waits until it is the player's move
    #Make move here