import pygame
import Settings
from Piece import *
from Move import *

class Chess:
    settings = Settings.Settings()

    def generateBoard(self, FEN):
        self.allMoves = [[],[]]
        self.turn = self.settings.WHITE
        self.Kings = [None, None]
        self.board = [
            [Empty(None, (i, j), self) for j in range(8)] for i in range(8)
        ]
        i = 0
        j = 0
        parts = FEN.split(" ")
        for c in parts[0]:
            if c == '/':
                i += 1
                j = 0
            elif c.isdigit():
                j += int(c)
            elif c.islower():
                self.board[7-i][j] = self.pieceDict[c.upper()](self.settings.BLACK, (7-i, j), self)
                j += 1
            else:
                self.board[7-i][j] = self.pieceDict[c](self.settings.WHITE, (7-i, j), self)
                j += 1
        
        self.halfMoves = int(parts[-2])
        self.totalMoves = int(parts[-1])
        if parts[1] == "w":
            self.turn = self.settings.WHITE
        else:
            self.turn = self.settings.BLACK
        
        for i in range(8):
            for j in range(8):
                if self.board[i][j].__class__.__name__ == "King":
                    self.Kings[self.board[i][j].color] = self.board[i][j]
                if self.board[i][j].__class__.__name__ == "Rook":
                    self.board[i][j].moved = self.totalMoves

        self.moves_generated = [[],[]]
    
        for x in parts[2]:
            if x == 'K':
                self.board[0][7].moved = 0
            elif x == 'Q':
                self.board[0][0].moved = 0
            elif x == 'k':
                self.board[7][7].moved = 0
            elif x == 'q':
                self.board[7][0].moved = 0
        
        if len(parts) == 6 and parts[3] != '-':
            cell = (int(parts[3][1]) - 1, ord(parts[3][0]) - ord('a'))
            if self.turn == self.settings.WHITE:
                self.allMoves.append(Move(Pawn(self.settings.BLACK, (cell[0] + 1, cell[1]), self), Empty(None, (cell[0] - 1, cell[1]), self)))
            else:
                self.allMoves.append(Move(Pawn(self.settings.WHITE, (cell[0] - 1, cell[1]), self), Empty(None, (cell[0] + 1, cell[1]), self)))
        


    def __init__(self):
        self.pieceDict = {
            "P": Pawn,
            "R": Rook,
            "N": Knight,
            "B": Bishop,
            "Q": Queen,
            "K": King
        }
        self.generateBoard("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        self.generateBoard("3rr3/4k3/3qbp1Q/pRpp4/p3pP2/2PBB1Pp/2P5/R5K1 b - - 0 33")

    def getPiece(self, position):
        return self.board[position[0]][position[1]]
    
    def promote(self, position, piece):
        if piece.__class__.__name__ == "Pawn" and (position[0] == 0 or position[0] == 7):
            temp = Queen(piece.color, position, self)
            temp.moved = piece.moved
            return temp
        return piece
    
    def movePiece(self, position, piece):
        piece = self.promote(position, piece)
        self.board[position[0]][position[1]] = piece
        piece.move(position)
    
    
    def undomovePiece(self, position, piece):
        self.board[position[0]][position[1]] = piece
        piece.undomove(position)

    def changeTurn(self):
        self.turn = 1 - self.turn

    def move(self, move):
        self.allMoves.append(move.copy())
        self.movePiece(move.to_square.position, move.from_square.copy())
        self.movePiece(move.from_square.position, Empty(None, move.from_square.position, self))
        if move.__class__.__name__ == "Castle":
            self.movePiece(move.rook_to_square.position, move.rook_from_square.copy())
            self.movePiece(move.rook_from_square.position, Empty(None, move.rook_from_square.position, self))
        if move.__class__.__name__ == "EnPassant":
            self.movePiece(move.capture_square.position, Empty(None, move.capture_square.position, self))
        self.changeTurn()
        if self.turn == self.settings.WHITE:
            self.totalMoves += 1
    
    def undoMove(self):
        move = self.allMoves.pop()
        if move.__class__.__name__ == "Castle":
            self.undomovePiece(move.rook_from_square.position, move.rook_from_square)
            self.undomovePiece(move.rook_to_square.position, Empty(None, move.rook_to_square.position, self))
        if move.__class__.__name__ == "EnPassant":
            self.undomovePiece(move.capture_square.position,move.capture_square)
        self.undomovePiece(move.from_square.position, move.from_square)
        self.undomovePiece(move.to_square.position, move.to_square)
        self.changeTurn()
        if len(self.moves_generated[0]) > 0 and self.totalMoves == self.moves_generated[0][-1]:
            self.moves_generated[0].pop()
            self.allMoves[0].pop()
        if len(self.moves_generated[1]) > 0 and self.totalMoves == self.moves_generated[1][-1]:
            self.moves_generated[1].pop()
            self.allMoves[1].pop()
        if self.turn == self.settings.BLACK:
            self.totalMoves -= 1

    def getMoves(self, piece, checkCheck):
        if piece.color != self.turn:
            return []
        return piece.getMoves(checkCheck)
    
    def getAllMoves(self, checkCheck):
        if len(self.moves_generated[checkCheck]) == 0 or self.moves_generated[checkCheck] != self.totalMoves:
            moves = []
            for row in self.board:
                for piece in row:
                    moves += self.getMoves(piece, checkCheck)
            self.moves_generated[checkCheck].append(self.totalMoves)
            self.allMoves[checkCheck].append(moves)
        return self.allMoves[checkCheck][-1]
    
    def checkIfAnyMove(self):
        for row in self.board:
            for piece in row:
                if piece.color == self.turn and len(self.getMoves(piece, checkCheck=True)) > 0:
                    return True
        return False
    

    def evaluate(self):
        if self.checkIfCheckMate():
            return float(-100000000)
        if self.checkIfStaleMate():
            return 0
        score = 0
        for row in self.board:
            for piece in row:
                if piece.color == self.turn:
                    score += piece.score * 3
                    score += piece.positional_score[piece.position[0]][piece.position[1]]
                elif piece.color != None:
                    score -= piece.score * 3
                    score -= piece.positional_score[piece.position[0]][piece.position[1]]
                

        # print(score)
        return score
    
    def adjustKings(self):
        if self.board[self.Kings[0].position[0]][self.Kings[0].position[1]].__class__.__name__ != "King" or self.board[self.Kings[0].position[0]][self.Kings[0].position[1]].color != self.settings.WHITE or self.board[self.Kings[1].position[0]][self.Kings[1].position[1]].__class__.__name__ != "King" or self.board[self.Kings[1].position[0]][self.Kings[1].position[1]].color != self.settings.BLACK:
            done = 0
            for i in range(8):
                for j in range(8):
                    if self.board[i][j].__class__.__name__ == "King" and self.board[i][j].color == self.settings.WHITE:
                        self.Kings[0] = self.board[i][j]
                        done += 1
                    if self.board[i][j].__class__.__name__ == "King" and self.board[i][j].color == self.settings.BLACK:
                        self.Kings[1] = self.board[i][j]
                        done += 1
                    if done == 2:
                        return
                    
    def checkIfSelfCheck(self):
        # for move in self.getAllMoves(checkCheck=False):
        #     if move.to_square.__class__.__name__ == "King" and move.to_square.color != self.turn:
        #         return True
        # Check if the king is in check by Pawns
        self.adjustKings()
        if self.turn == self.settings.WHITE:
            i = self.Kings[self.turn].position[0] + 1
            j = self.Kings[self.turn].position[1] + 1
            if i < 8 and j < 8 and self.board[i][j].color == self.settings.BLACK and self.board[i][j].__class__.__name__ == "Pawn":
                return True
            j -= 2
            if i < 8 and j >= 0 and self.board[i][j].color == self.settings.BLACK and self.board[i][j].__class__.__name__ == "Pawn":
                return True
        else:
            i = self.Kings[self.turn].position[0] - 1
            j = self.Kings[self.turn].position[1] + 1
            if i >= 0 and j < 8 and self.board[i][j].color == self.settings.WHITE and self.board[i][j].__class__.__name__ == "Pawn":
                return True
            j -= 2
            if i >= 0 and j >= 0 and self.board[i][j].color == self.settings.WHITE and self.board[i][j].__class__.__name__ == "Pawn":
                return True

        # Check if the king is in check by Knights
        for di in range(-2, 3):
            for dj in range(-2, 3):
                if abs(di) + abs(dj) == 3:
                    i = self.Kings[self.turn].position[0] + di
                    j = self.Kings[self.turn].position[1] + dj
                    if i >= 0 and i < 8 and j >= 0 and j < 8 and self.board[i][j].color != self.turn and self.board[i][j].__class__.__name__ == "Knight":
                        return True

        # Check if the king is in check by Rooks, Queens and Bishops
        for di in range(-1, 2):
            for dj in range(-1, 2):
                if abs(di) + abs(dj) == 1:
                    i = self.Kings[self.turn].position[0] + di
                    j = self.Kings[self.turn].position[1] + dj
                    while i >= 0 and i < 8 and j >= 0 and j < 8:
                        if self.board[i][j].color != None:
                            if self.board[i][j].color != self.turn and (self.board[i][j].__class__.__name__ == "Queen" or self.board[i][j].__class__.__name__ == "Rook"):
                                return True
                            break
                        i += di
                        j += dj
                
                if abs(di) + abs(dj) == 2:
                    i = self.Kings[self.turn].position[0] + di
                    j = self.Kings[self.turn].position[1] + dj
                    while i >= 0 and i < 8 and j >= 0 and j < 8:
                        if self.board[i][j].color != None:
                            if self.board[i][j].color != self.turn and (self.board[i][j].__class__.__name__ == "Queen" or self.board[i][j].__class__.__name__ == "Bishop"):
                                return True
                            break
                        i += di
                        j += dj
        # Check if the king is in check by Kings
        if max([abs(self.Kings[self.turn].position[0] - self.Kings[1 - self.turn].position[0]), abs(self.Kings[self.turn].position[1] - self.Kings[1 - self.turn].position[1])]) <= 1:
            return True

        return False
    
    def checkIfCheck(self):
        self.changeTurn()
        res = self.checkIfSelfCheck()
        self.changeTurn()
        return res
    
    
    
    def checkIfCheckMate(self):
        if not self.checkIfAnyMove() and self.checkIfSelfCheck():
            return True
        return False
    
    def checkIfStaleMate(self):
        if not self.checkIfAnyMove() and not self.checkIfSelfCheck():
            return True
        return False
    
    
