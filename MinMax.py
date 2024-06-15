class MinMax:
    def __init__(self, chess, depth):
        self.chess = chess
        self.depth = depth
        self.bestMove = None
        self.bestScore = None
        self.explored = 0

    def getBestMove(self):
        self.minimax(self.depth, self.chess, True)
        return self.bestMove
    
    def minimax(self, depth, chess, maximizingPlayer):
        if depth == 0:
            if self.depth % 2 == 0:
                return chess.evaluate()
            else:
                return -chess.evaluate()
        self.explored += 1
        moves = chess.getAllMoves(checkCheck=True)
        if maximizingPlayer:
            maxEval = float('-inf')
            for move in moves:
                chess.move(move)
                eval = self.minimax(depth - 1, chess, False)
                if eval >= maxEval:
                    maxEval = eval
                    if depth == self.depth:
                        self.bestMove = move
                        self.bestScore = maxEval
                chess.undoMove()
            return maxEval
        else:
            minEval = float('inf')
            for move in moves:
                chess.move(move)
                eval = self.minimax(depth - 1, chess, True)
                if eval < minEval:
                    minEval = eval
                chess.undoMove()
            return minEval
