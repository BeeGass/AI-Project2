"""
Psuedo code for MiniMax

function Minimax(position, depth, maximizingPlayer)
    if depth == 0 or game over in position then
        return static evaluation of position
    if maximizingPlayer then
        maxEval = −∞
        each child in position
        eval = Minimax(child, depth-1, false)
        maxEval = max(maxEval, eval)
        return maxEval
    else
        minEval = +∞
        each child in position
        eval = Minimax(child, depth-1, true)
        minEval = min(minEval, eval)
        return minEval


Psuedo code for alpha beta pruning

function Minimax(position, depth, alpha, deta, maximizingPlayer)
    if depth == 0 or game over in position then
        return static evaluation of position
    if maximizingPlayer then
        each child in position
        eval = Minimax(child, depth-1, false)
        maxEval = max(maxEval, eval) alpha= max(alpha, eval)
        if beta ≤ alpha break
            return maxEval
    else
        each child in position
        eval = Minimax(child, depth-1, true)
        minEval = min(minEval, eval) beta= max(beta, eval)
    if beta ≤ alpha break
        return minEval
"""