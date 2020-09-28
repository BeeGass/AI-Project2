class Board:
    boardSize = 15
    board: list
    def __init__(self):
        self.board = [[0 for x in range(boardSize)] for y in range(boardSize)]
        #initializes a 15x15 board
        #0 represents an empty space, 1 represents a space occupied by the AI player, and 2 represents a space occupied by the
        #opposing player

    #Places a piece on the board
    #row: The row
    #col: The column
    #Player: 1 if AI player, 2 if opponent
    def placePiece(row, col, player):
        board[row,col] = player
        pass