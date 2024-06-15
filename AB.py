import random
class AlphaBeta:
    def __init__(self, chess, depth):
        self.chess = chess
        self.depth = depth
        self.bestMove = None
        self.bestScore = None
        self.K = 20
        self.explored = 0

    def getBestMove(self):
        self.alphabeta(self.depth, self.chess, True, float('-inf'), float('inf'))
        return self.bestMove
    
    def alphabeta(self, depth, chess, maximizingPlayer, alpha, beta):
        if depth == 0:
            if maximizingPlayer:
                return chess.evaluate()
            else:
                return -chess.evaluate()
        self.explored += 1
        moves = chess.getAllMoves(checkCheck=True)
        if len(moves) == 0:
            if maximizingPlayer:
                return chess.evaluate()
            else:
                return -chess.evaluate()
            
        # def func(x):
        #     chess.move(x)
        #     score = -chess.evaluate()
        #     chess.undoMove()
        #     return score

        # moves = sorted(moves, key= lambda x: func(x))

        # random.shuffle(moves) 
        
        # moves = moves[:self.K]
        if maximizingPlayer:
            maxEval = float('-inf')
            for move in moves:
                chess.move(move)
                eval = self.alphabeta(depth - 1, chess, False, alpha, beta)
                chess.undoMove()
                if eval >= maxEval:
                    maxEval = eval
                    if depth == self.depth:
                        self.bestMove = move
                        self.bestScore = maxEval
                alpha = max(alpha, eval)
                if beta < alpha:
                    break
            return maxEval
        else:
            minEval = float('inf')
            for move in moves:
                chess.move(move)
                eval = self.alphabeta(depth - 1, chess, True, alpha, beta)
                chess.undoMove()
                if eval < minEval:
                    minEval = eval
                beta = min(beta, eval)
                if beta < alpha:
                    break
            return minEval
