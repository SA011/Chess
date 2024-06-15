import Settings
from Move import *
class ChessPiece:
    settings = Settings.Settings()
    def __init__(self, color, position, chess):
        self.color = color
        self.position = position
        self.score = 0
        self.image = None
        self.chess = chess
        self.moved = 0
        if self.__class__.__name__ != "Empty":
            self.score = self.settings.pieceScore[self.__class__.__name__]
            if color == self.settings.BLACK:
                self.image = self.settings.piecesImages[self.__class__.__name__.lower()]
            if color == self.settings.WHITE:
                self.image = self.settings.piecesImages[self.__class__.__name__.upper()]

    def move(self, position):
        self.position = position
        self.moved += 1

    
    def undomove(self, position):
        self.position = position

    

    def getMoves(self, checkCheck):
        return []
    
    def copy(self):
        temp = self.__class__(self.color, self.position, self.chess)
        temp.moved = self.moved
        return temp

    def __str__(self):
        return str(self.color) + " " + self.__class__.__name__ + " at " + str(self.position)

class King(ChessPiece):
    def __init__(self, color, position, chess):
        super().__init__(color, position, chess)
        if color == self.settings.BLACK:
            self.positional_score = [
                [-30, -40, -40, -50, -50, -40, -40, -30],  # 8th rank (1st for white) - Restricted on edge
                [-30, -40, -40, -50, -50, -40, -40, -30],  # 7th rank (2nd for white) - Restricted on edge
                [-30, -40, -40, -50, -50, -40, -40, -30],  # 6th rank (3rd for white) - Restricted on edge
                [-30, -40, -40, -50, -50, -40, -40, -30],  # 5th rank (4th for white) - Restricted on edge
                [-20, -30, -30, -40, -40, -30, -30, -20],  # 4th rank (5th for white) - Restricted on edge
                [-10, -20, -20, -30, -30, -20, -20, -10],  # 3rd rank (6th for white) - Restricted on edge
                [20,  20,   0,   0,   0,   0,  20,  20],  # 2nd rank (7th for white) - Restricted on edge
                [20,  30,  10,   0,   0,  10,  30,  20],  # 1st rank (8th for white) - Restricted on edge
            ]
        if color == self.settings.WHITE:
            self.positional_score = [
                [20,  30,  10,   0,   0,  10,  30,  20],  # 1st rank (8th for white) - Restricted on edge
                [20,  20,   0,   0,   0,   0,  20,  20],  # 2nd rank (7th for white) - Restricted on edge
                [-10, -20, -20, -30, -30, -20, -20, -10],  # 3rd rank (6th for white) - Restricted on edge
                [-20, -30, -30, -40, -40, -30, -30, -20],  # 4th rank (5th for white) - Restricted on edge
                [-30, -40, -40, -50, -50, -40, -40, -30],  # 5th rank (4th for white) - Restricted on edge
                [-30, -40, -40, -50, -50, -40, -40, -30],  # 6th rank (3rd for white) - Restricted on edge
                [-30, -40, -40, -50, -50, -40, -40, -30],  # 7th rank (2nd for white) - Restricted on edge
                [-30, -40, -40, -50, -50, -40, -40, -30],  # 8th rank (1st for white) - Restricted on edge
            ]
    def getMoves(self, checkCheck):
        moves = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                new_position = (self.position[0] + i, self.position[1] + j)
                if self.settings.checkPosition(new_position):
                    piece = self.chess.getPiece(new_position)
                    if piece.color != self.color:
                        if checkCheck:
                            self.chess.move(Move(self, piece))
                            if not self.chess.checkIfCheck():
                                moves.append(Move(self, piece))
                            self.chess.undoMove()
                        else:
                            moves.append(Move(self, piece))
        
        # Castling
        if checkCheck and self.moved == 0 and not self.chess.checkIfSelfCheck():
            for i in [-1, 1]:
                rook = self.chess.getPiece((self.position[0], 0 if i == -1 else 7))
                if rook.__class__.__name__ == "Rook" and rook.moved == 0:
                    can_castle = True
                    for j in range(1, 4):
                        piece = self.chess.getPiece((self.position[0], self.position[1] + i * j))
                        if piece.color != None and piece != rook:
                            can_castle = False
                            break
                    if can_castle:
                        # Check if the king is not in check in the squares it will pass through
                        for j in range(1, 3):
                            self.chess.move(Move(self, self.chess.getPiece((self.position[0], self.position[1] + i * j))))
                            if self.chess.checkIfCheck():
                                can_castle = False
                            self.chess.undoMove()
                            if not can_castle:
                                break
                        if can_castle:
                            piece = self.chess.getPiece((self.position[0], self.position[1] + i * 2))
                            rook_piece = self.chess.getPiece((self.position[0], self.position[1] + i))
                            self.chess.move(Castle(self, piece, rook, rook_piece))
                            if not self.chess.checkIfCheck():
                                moves.append(Castle(self, piece, rook, rook_piece))
                            self.chess.undoMove()
    
        return moves
    
class Queen(ChessPiece):
    def __init__(self, color, position, chess):
        super().__init__(color, position, chess)
        if color == self.settings.BLACK:
            self.positional_score = [
                [-20, -10,  0,  10,  10,  0, -10, -20],  # 8th rank (1st for black) - Restricted on edge (some diagonals limited)
                [30,  40,  40,  50,  50,  40,  40,  30],  # 7th rank (2nd for white) - Decent squares on all diagonals
                [40,  50,  50,  60,  60,  50,  50,  40],  # 6th rank (3rd for white) - Good squares, especially on open diagonals
                [50,  60,  60,  70,  70,  60,  60,  50],  # 5th rank (4th for white) - Strong squares, especially on open diagonals
                [50,  60,  60,  70,  70,  60,  60,  50],  # 4th rank (5th for white) - Decent squares
                [40,  50,  50,  60,  60,  50,  50,  40],  # 3rd rank (6th for white) - Slightly restricted
                [30,  40,  40,  50,  50,  40,  40,  30],  # 2nd rank (7th for white) - More restricted on edge
                [-10, -10,  0,   0,   0,   0, -10, -10],  # 1st rank (8th for white) - Starting rank (low value)
            ]
        if color == self.settings.WHITE:
            self.positional_score = [
                [-10, -10,  0,   0,   0,   0, -10, -10],  # 1st rank (8th for white) - Starting rank (low value)
                [30,  40,  40,  50,  50,  40,  40,  30],  # 2nd rank (7th for white) - More restricted on edge
                [40,  50,  50,  60,  60,  50,  50,  40],  # 3rd rank (6th for white) - Slightly restricted
                [50,  60,  60,  70,  70,  60,  60,  50],  # 4th rank (5th for white) - Decent squares
                [50,  60,  60,  70,  70,  60,  60,  50],  # 5th rank (4th for white) - Strong squares, especially on open diagonals
                [40,  50,  50,  60,  60,  50,  50,  40],  # 6th rank (3rd for white) - Good squares, especially on open diagonals
                [30,  40,  40,  50,  50,  40,  40,  30],  # 7th rank (2nd for white) - Decent squares on all diagonals
                [-20, -10,  0,  10,  10,  0, -10, -20],  # 8th rank (1st for black) - Restricted on edge (some diagonals limited)
            ]

    def getMoves(self, checkCheck):
        moves = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                for k in range(1, 8):
                    new_position = (self.position[0] + i * k, self.position[1] + j * k)
                    if self.settings.checkPosition(new_position):
                        piece = self.chess.getPiece(new_position)
                        if piece.color != self.color:
                            if checkCheck:
                                self.chess.move(Move(self, piece))
                                if not self.chess.checkIfCheck():
                                    moves.append(Move(self, piece))
                                self.chess.undoMove()
                            else:
                                moves.append(Move(self, piece))
                        if piece.color != None:
                            break
                    else:
                        break
        return moves
class Bishop(ChessPiece):
    def __init__(self, color, position, chess):
        super().__init__(color, position, chess)
        if color == self.settings.BLACK:
            self.positional_score = [
                [-20, -10,  0,  10,  10,  0, -10, -20],  # 8th rank (1st for black) - Restricted on edge (diagonals limited)
                [20,  30,  30,  40,  40,  30,  30,  20],  # 7th rank (2nd for white) - Decent squares on long diagonals
                [30,  40,  40,  50,  50,  40,  40,  30],  # 6th rank (3rd for white) - Good squares, especially on open diagonals
                [40,  50,  50,  60,  60,  50,  50,  40],  # 5th rank (4th for white) - Strong squares, especially on open diagonals
                [40,  50,  50,  60,  60,  50,  50,  40],  # 4th rank (5th for white) - Decent squares
                [30,  40,  40,  50,  50,  40,  40,  30],  # 3rd rank (6th for white) - Slightly restricted
                [20,  30,  30,  40,  40,  30,  30,  20],  # 2nd rank (7th for white) - More restricted on edge
                [-10, -10,  0,   0,   0,   0, -10, -10],  # 1st rank (8th for white) - Starting rank (low value)
            ]
        if color == self.settings.WHITE:
            self.positional_score = [
                [-10, -10,  0,   0,   0,   0, -10, -10],  # 1st rank (8th for white) - Starting rank (low value)
                [20,  30,  30,  40,  40,  30,  30,  20],  # 2nd rank (7th for white) - More restricted on edge
                [30,  40,  40,  50,  50,  40,  40,  30],  # 3rd rank (6th for white) - Slightly restricted
                [40,  50,  50,  60,  60,  50,  50,  40],  # 4th rank (5th for white) - Decent squares
                [40,  50,  50,  60,  60,  50,  50,  40],  # 5th rank (4th for white) - Strong squares, especially on open diagonals
                [30,  40,  40,  50,  50,  40,  40,  30],  # 6th rank (3rd for white) - Good squares, especially on open diagonals
                [20,  30,  30,  40,  40,  30,  30,  20],  # 7th rank (2nd for white) - Decent squares on long diagonals
                [-20, -10,  0,  10,  10,  0, -10, -20],  # 8th rank (1st for black) - Restricted on edge (diagonals limited)
            ]           

    
    def getMoves(self, checkCheck):
        moves = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 or j == 0:
                    continue
                for k in range(1, 8):
                    new_position = (self.position[0] + i * k, self.position[1] + j * k)
                    if self.settings.checkPosition(new_position):
                        piece = self.chess.getPiece(new_position)
                        if piece.color != self.color:
                            if checkCheck:
                                self.chess.move(Move(self, piece))
                                if not self.chess.checkIfCheck():
                                    moves.append(Move(self, piece))
                                self.chess.undoMove()
                            else:
                                moves.append(Move(self, piece))
                        if piece.color != None:
                            break
                    else:
                        break
        return moves

class Knight(ChessPiece):
    def __init__(self, color, position, chess):
        super().__init__(color, position, chess)
        if self.color == self.settings.BLACK:
            self.positional_score = [
                [-20, -10,  0,  10,  10,  0, -10, -20],  # 8th rank (1st for black) - Restricted on edge
                [20,  30,  30,  40,  40,  30,  30,  20],  # 7th rank (2nd for white) - Good outpost squares
                [30,  40,  40,  50,  50,  40,  40,  30],  # 6th rank (3rd for white) - Strong central squares
                [30,  40,  50,  50,  50,  50,  40,  30],  # 5th rank (4th for white) - Decent squares
                [20,  30,  40,  40,  40,  40,  30,  20],  # 4th rank (5th for white) - Standard squares
                [10,  20,  30,  30,  30,  30,  20,  10],  # 3rd rank (6th for white) - Slightly restricted
                [0,   0,   0,   0,   0,   0,   0,   0],  # 2nd rank (7th for white) - Very restricted on edge
                [-10, -10,  0,   0,   0,   0, -10, -10],  # 1st rank (8th for white) - Starting rank (low value)
            ]
        if self.color == self.settings.WHITE:
            self.positional_score = [
                [-10, -10,  0,  0,  0,  0, -10, -10],  # 1st rank (8th for white) - Starting rank (low value)
                [0,   0,   0,   0,   0,   0,   0,   0],  # 2nd rank (7th for white) - Very restricted on edge
                [10,  20,  30,  30,  30,  30,  20,  10],  # 3rd rank (6th for white) - Slightly restricted
                [20,  30,  40,  40,  40,  40,  30,  20],  # 4th rank (5th for white) - Standard squares
                [30,  40,  50,  50,  50,  50,  40,  30],  # 5th rank (4th for white) - Decent squares
                [30,  40,  40,  50,  50,  40,  40,  30],  # 6th rank (3rd for white) - Strong central squares
                [20,  30,  30,  40,  40,  30,  30,  20],  # 7th rank (2nd for white) - Good outpost squares
                [-20, -10,  0,  10,  10,  0, -10, -20],  # 8th rank (1st for black) - Restricted on edge
            ]

    def getMoves(self, checkCheck):
        moves = []
        for i in range(-2, 3):
            for j in range(-2, 3):
                if abs(i) + abs(j) == 3:
                    new_position = (self.position[0] + i, self.position[1] + j)
                    if self.settings.checkPosition(new_position):
                        piece = self.chess.getPiece(new_position)
                        if piece.color != self.color:
                            if checkCheck:
                                self.chess.move(Move(self, piece))
                                if not self.chess.checkIfCheck():
                                    moves.append(Move(self, piece))
                                self.chess.undoMove()
                            else:
                                moves.append(Move(self, piece))
        return moves
    

class Rook(ChessPiece):
    def __init__(self, color, position, chess):
        super().__init__(color, position, chess)   
        if color == self.settings.BLACK:
            #Black rooks most suitable positions
            self.positional_score = [
                [-40, -20,  0,  20,  20,  0, -20, -40],  # 8th rank (1st for white) 
                [100,  80,  60,  40,  40,  60,  80, 100],  # 7th rank (2nd for white) - Most control
                [-70, -50, -30, -10, -10, -30, -50, -70],  # 6th rank (3rd for white)
                [-40, -20,  0,  20,  20,  0, -20, -40],  # 5th rank (4th for white)
                [-40, -20,  0,  20,  20,  0, -20, -40],  # 4th rank
                [-40, -20,  0,  20,  20,  0, -20, -40],  # 3rd rank
                [-70, -50, -30, -10, -10, -30, -50, -70],  # 2nd rank (7th for white)
                [-40, -20,  0,  20,  20,  0, -20, -40],  # 1st rank (8th for white)
            ]
        if color == self.settings.WHITE:
            #White rooks most suitable positions
            self.positional_score = [
                [-40, -20,  0,  20,  20,  0, -20, -40],  # 1st rank
                [-70, -50, -30, -10, -10, -30, -50, -70],  # 2nd rank
                [-40, -20,  0,  20,  20,  0, -20, -40],  # 3rd rank
                [-40, -20,  0,  20,  20,  0, -20, -40],  # 4th rank
                [-40, -20,  0,  20,  20,  0, -20, -40],  # 5th rank
                [-40, -20,  0,  20,  20,  0, -20, -40],  # 6th rank
                [100,  80,  60,  40,  40,  60,  80, 100],  # 7th rank - Most control
                [-40, -20,  0,  20,  20,  0, -20, -40],  # 8th rank
            ]

    def getMoves(self, checkCheck):
        moves = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i != 0 and j != 0 or i == j:
                    continue
                for k in range(1, 8):
                    new_position = (self.position[0] + i * k, self.position[1] + j * k)
                    if self.settings.checkPosition(new_position):
                        piece = self.chess.getPiece(new_position)
                        if piece.color != self.color:
                            if checkCheck:
                                self.chess.move(Move(self, piece))
                                if not self.chess.checkIfCheck():
                                    moves.append(Move(self, piece))
                                self.chess.undoMove()
                            else:
                                moves.append(Move(self, piece))
                        if piece.color != None:
                            break
                    else:
                        break
        return moves

class Pawn(ChessPiece):
    def __init__(self, color, position, chess):
        super().__init__(color, position, chess)
        if color == self.settings.BLACK:
            #Black pawns most suitable positions
            self.positional_score = [
                [0,  20,  30,  40,  40,  30,  20,  0],  # 8th rank (1st for white) - Promotion rank (highest value)
                [50,  50,  50,  50,  50,  50,  50,  50],  # 7th rank (2nd for white) - Strong advanced position
                [30,  30,  30,  30,  30,  30,  30,  30],  # 6th rank (3rd for white) - Decent advanced position
                [20,  20,  20,  20,  20,  20,  20,  20],  # 5th rank (4th for white) - Standard position
                [0,   0,   0,   0,   0,   0,   0,   0],  # 4th rank (5th for white) - Unstable, pawn island penalty
                [0,   0,   0,   0,   0,   0,   0,   0],  # 3rd rank (6th for white) - Unstable, pawn island penalty
                [-20, -20, -20, -20, -20, -20, -20, -20],  # 2nd rank (7th for white) - Isolated pawn penalty
                [-40, -40, -40, -40, -40, -40, -40, -40],  # 1st rank (8th for white) 
            ]
        if color == self.settings.WHITE:
            #White pawns most suitable positions
            self.positional_score = [
                [-40, -40, -40, -40, -40, -40, -40, -40],  # 1st rank
                [-20, -20, -20, -20, -20, -20, -20, -20],  # 2nd rank
                [0,   0,   0,   0,   0,   0,   0,   0],  # 3rd rank
                [0,   0,   0,   0,   0,   0,   0,   0],  # 4th rank
                [20,  20,  20,  20,  20,  20,  20,  20],  # 5th rank
                [30,  30,  30,  30,  30,  30,  30,  30],  # 6th rank
                [50,  50,  50,  50,  50,  50,  50,  50],  # 7th rank - Strong advanced position
                [0,  20,  30,  40,  40,  30,  20,  0],  # 8th rank - Promotion rank (highest value)
            ]


    def getMoves(self, checkCheck):
        moves = []
        direction = 1
        if self.color == self.settings.BLACK:
            direction = -1
        new_position = (self.position[0] + direction, self.position[1])
        if checkCheck and self.settings.checkPosition(new_position):
            piece = self.chess.getPiece(new_position)
            if piece.color == None:
                moving = Move(self, piece)
                self.chess.move(moving)
                if not self.chess.checkIfCheck():
                    moves.append(moving)
                self.chess.undoMove()
                if self.color == self.settings.BLACK and self.position[0] == 6 or self.color == self.settings.WHITE and self.position[0] == 1:
                    new_position = (self.position[0] + 2 * direction, self.position[1])
                    if self.settings.checkPosition(new_position):
                        piece = self.chess.getPiece(new_position)
                        if piece.color == None:
                            self.chess.move(Move(self, piece))
                            if not self.chess.checkIfCheck():
                                moves.append(Move(self, piece))
                            self.chess.undoMove()
        for i in [-1, 1]:
            new_position = (self.position[0] + direction, self.position[1] + i)
            if self.settings.checkPosition(new_position):
                piece = self.chess.getPiece(new_position)
                if piece.color != self.color and piece.color != None:
                    if checkCheck:
                        self.chess.move(Move(self, piece))
                        if not self.chess.checkIfCheck():
                            moves.append(Move(self, piece))
                        self.chess.undoMove()
                    else:
                        moves.append(Move(self, piece))
        
        # En passant
        if checkCheck and self.position[0] == 3.5 + 0.5 * direction and self.chess.allMoves != []:
            for i in [-1, 1]:
                new_position = (self.position[0], self.position[1] + i)
                if self.settings.checkPosition(new_position):
                    piece = self.chess.getPiece(new_position)
                    if piece.color != self.color and piece.color != None and piece.__class__.__name__ == "Pawn":
                        if self.chess.allMoves[-1].to_square.position == piece.position and self.chess.allMoves[-1].from_square.position == (piece.position[0] + 2 * direction, piece.position[1]):
                            piece2 = self.chess.getPiece((piece.position[0] + direction, piece.position[1]))
                            self.chess.move(EnPassant(self, piece2, piece))
                            if not self.chess.checkIfCheck():
                                moves.append(EnPassant(self, piece2, piece))
                            self.chess.undoMove()
        return moves

class Empty(ChessPiece):
    def __init__(self, color, position, chess):
        super().__init__(color, position, chess)
