import pygame
from Settings import Settings

class Chess:
    def __init__(self, caption):
        pygame.init()
        self.settings = Settings()
        self.caption = caption
        self.screen = pygame.display.set_mode(self.settings.screen)
        pygame.display.set_caption(caption)
        self.turn = 0

        self.board = [
            ["r", "n", "b", "q", "k", "b", "n", "r"],
            ["p" for i in range(8)],
            ["." for i in range(8)],
            ["." for i in range(8)],
            ["." for i in range(8)],
            ["." for i in range(8)],
            ["P" for i in range(8)],
            ["R", "N", "B", "Q", "K", "B", "N", "R"]
        ]

        self.selected = [
            [0 for i in range(8)] for j in range(8)   
        ]

        self.selectedPiece = (0, 0)

        self.capturedPieces = [
            [],
            []
        ]

        self.checkmated = False
    

    def handleDownKey(self, event):
        pass
    def handleUpKey(self, event):
        pass            

    def isKingOnCheck(self, x, y):
        # print(x, y)
        p = self.board[y][x]
        self.board[y][x] = "."
        for i in range(8):
            for j in range(8):
                if self.board[i][j].islower() ^ self.turn:
                    temp = self.selected.copy()
                    self.selected = [[0 for i in range(8)] for j in range(8)]
                    self.show_moves(self.board[i][j], j, i, True)
                    if self.selected[y][x] == 2:
                        self.selected = temp
                        self.board[y][x] = p
                        return True
                    self.selected = temp
        self.board[y][x] = p
        return False
    

    def show_moves(self, piece, x, y, onlyAttacks = False):
        if piece == "P":
            if y > 0 and self.board[y - 1][x] == ".":
                self.selected[y - 1][x] = 2
                if y == 6 and self.board[y - 2][x] == ".":
                    self.selected[y - 2][x] = 2
            if y > 0 and x > 0 and (self.board[y - 1][x - 1] != "."  and self.board[y - 1][x - 1].islower() or onlyAttacks):
                self.selected[y - 1][x - 1] = 2
            if y > 0 and x < 7 and (self.board[y - 1][x + 1] != "." and self.board[y - 1][x + 1].islower() or onlyAttacks):
                self.selected[y - 1][x + 1] = 2
        if piece == "p":
            if y < 7 and self.board[y + 1][x] == ".":
                self.selected[y + 1][x] = 2
                if y == 1 and self.board[y + 2][x] == ".":
                    self.selected[y + 2][x] = 2
            if y < 7 and x > 0 and (self.board[y + 1][x - 1] != "." and self.board[y + 1][x - 1].isupper() or onlyAttacks):
                self.selected[y + 1][x - 1] = 2
            if y < 7 and x < 7 and (self.board[y + 1][x + 1] != "." and self.board[y + 1][x + 1].isupper() or onlyAttacks):
                self.selected[y + 1][x + 1] = 2

        if piece == "R" or piece == "r":
            for move in self.settings.moves[piece]:
                for i in range(1, 8):
                    if x + move[0] * i < 0 or x + move[0] * i > 7 or y + move[1] * i < 0 or y + move[1] * i > 7:
                        break
                    if self.board[y + move[1] * i][x + move[0] * i] == ".":
                        self.selected[y + move[1] * i][x + move[0] * i] = 2
                    else:
                        if piece.isupper() ^ self.board[y + move[1] * i][x + move[0] * i].isupper():
                            self.selected[y + move[1] * i][x + move[0] * i] = 2
                        break
        if piece == "N" or piece == "n":
            for move in self.settings.moves[piece]:
                if x + move[0] < 0 or x + move[0] > 7 or y + move[1] < 0 or y + move[1] > 7:
                    continue
                if self.board[y + move[1]][x + move[0]] == ".":
                    self.selected[y + move[1]][x + move[0]] = 2
                else:
                    if piece.isupper() ^ self.board[y + move[1]][x + move[0]].isupper():
                        self.selected[y + move[1]][x + move[0]] = 2
        if piece == "B" or piece == "b":
            for move in self.settings.moves[piece]:
                for i in range(1, 8):
                    if x + move[0] * i < 0 or x + move[0] * i > 7 or y + move[1] * i < 0 or y + move[1] * i > 7:
                        break
                    if self.board[y + move[1] * i][x + move[0] * i] == ".":
                        self.selected[y + move[1] * i][x + move[0] * i] = 2
                    else:
                        if piece.isupper() ^ self.board[y + move[1] * i][x + move[0] * i].isupper():
                            self.selected[y + move[1] * i][x + move[0] * i] = 2
                        break
        if piece == "Q" or piece == "q":
            for move in self.settings.moves[piece]:
                for i in range(1, 8):
                    if x + move[0] * i < 0 or x + move[0] * i > 7 or y + move[1] * i < 0 or y + move[1] * i > 7:
                        break
                    if self.board[y + move[1] * i][x + move[0] * i] == ".":
                        self.selected[y + move[1] * i][x + move[0] * i] = 2
                    else:
                        if piece.isupper() ^ self.board[y + move[1] * i][x + move[0] * i].isupper():
                            self.selected[y + move[1] * i][x + move[0] * i] = 2
                        break
            for move in self.settings.moves[piece]:
                if x + move[0] < 0 or x + move[0] > 7 or y + move[1] < 0 or y + move[1] > 7:
                    continue
                if self.board[y + move[1]][x + move[0]] == ".":
                    self.selected[y + move[1]][x + move[0]] = 2
                else:
                    if piece.isupper() ^ self.board[y + move[1]][x + move[0]].isupper():
                        self.selected[y + move[1]][x + move[0]] = 2
        if piece == "K" or piece == "k":
            for move in self.settings.moves[piece]:
                if x + move[0] < 0 or x + move[0] > 7 or y + move[1] < 0 or y + move[1] > 7:
                    continue
                if self.board[y + move[1]][x + move[0]] == "." and (onlyAttacks or not self.isKingOnCheck(x + move[0], y + move[1])):
                    self.selected[y + move[1]][x + move[0]] = 2
                else:
                    if piece.isupper() ^ self.board[y + move[1]][x + move[0]].isupper() and (onlyAttacks or not self.isKingOnCheck(x + move[0], y + move[1])):
                        self.selected[y + move[1]][x + move[0]] = 2

    def check_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
            if event.type == pygame.MOUSEBUTTONUP and not self.checkmated:
                x, y = pygame.mouse.get_pos()
                x = (x - self.settings.boardOffset[0]) // self.settings.cellSize[0]
                y = (y - self.settings.boardOffset[1]) // self.settings.cellSize[1]
                if x < 0 or x > 7 or y < 0 or y > 7:
                    for i in range(8):
                        for j in range(8):
                            self.selected[i][j] = 0
                    continue
                
                x = int(x)
                y = int(y)
                val = self.selected[y][x]
                for i in range(8):
                    for j in range(8):
                        self.selected[i][j] = 0
            
                
                if val == 2:
                    a, b = self.board[y][x], self.board[self.selectedPiece[1]][self.selectedPiece[0]]
                    self.board[y][x] = self.board[self.selectedPiece[1]][self.selectedPiece[0]]
                    self.board[self.selectedPiece[1]][self.selectedPiece[0]] = "."
                    kingPos = (0, 0)
                    for i in range(8):
                        for j in range(8):
                            if self.board[i][j] == ("K" if self.turn == 0 else "k"):
                                kingPos = (j, i)
                
                    if self.isKingOnCheck(kingPos[0], kingPos[1]):
                        self.board[y][x], self.board[self.selectedPiece[1]][self.selectedPiece[0]] = a, b
                        print("Invalid move")
                        continue
                    self.board[y][x], self.board[self.selectedPiece[1]][self.selectedPiece[0]] = a, b
    
                    if self.board[y][x] != ".":
                        self.capturedPieces[self.turn].append(self.board[y][x])

                    self.board[y][x] = self.board[self.selectedPiece[1]][self.selectedPiece[0]]
                    self.board[self.selectedPiece[1]][self.selectedPiece[0]] = "."
                    self.turn = 1 - self.turn
                    if self.detect_checkmate():
                        print("Checkmate")
                        self.checkmated = True
                    # print(self.board)
                elif self.board[y][x] != "." and self.board[y][x].isupper() ^ self.turn:
                    self.selected[y][x] = 1
                    self.show_moves(self.board[y][x], x, y)
                    self.selectedPiece = (x, y)
                
    def detect_checkmate(self):
        for i in range(8):
            for j in range(8):
                if self.board[i][j].isupper() ^ self.turn:
                    self.selected = [[0 for t in range(8)] for t2 in range(8)]
                    self.show_moves(self.board[i][j], j, i)
                    for k in range(8):
                        for l in range(8):
                            if self.selected[l][k] == 2:
                                temp = self.board[i][j]
                                temp2 = self.board[l][k]
                                self.board[i][j] = "."
                                self.board[l][k] = temp
                                kingPos = (0, 0)
                                for m in range(8):
                                    for n in range(8):
                                        if self.board[m][n] == ("K" if self.turn == 0 else "k"):
                                            kingPos = (n, m)
                                if not self.isKingOnCheck(kingPos[0], kingPos[1]):
                                    # print("Not checkmate")
                                    # print(i, j, l, k)
                                    # print(temp, temp2)
                                    self.board[i][j] = temp
                                    self.board[l][k] = temp2
                                    self.selected = [[0 for t in range(8)] for t2 in range(8)]
                                    return False
                                self.board[i][j] = temp
                                self.board[l][k] = temp2
        return True


    def draw_board(self):
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 0:
                    color = self.settings.cellColorWhite
                else:
                    color = self.settings.cellColorBlack
                
                if self.selected[row][col] == 1:
                    # slight bluish color on top of the cell
                    color = (color[0] + self.settings.selectedColorChange[0], color[1] + self.settings.selectedColorChange[1], color[2] + self.settings.selectedColorChange[2])
                if self.selected[row][col] == 2:
                    # slight greenish color on top of the cell
                    color = (color[0] + self.settings.moveColorChange[0], color[1] + self.settings.moveColorChange[1], color[2] + self.settings.moveColorChange[2])
                
                pygame.draw.rect(self.screen, color, (col * self.settings.cellSize[0] + self.settings.boardOffset[0], row * self.settings.cellSize[1] + self.settings.boardOffset[1], self.settings.cellSize[0], self.settings.cellSize[1]))

                if self.board[row][col] != ".":
                    image = pygame.image.load(self.settings.piecesImages[self.board[row][col]]).convert_alpha()
                    image = pygame.transform.scale(image, self.settings.cellSize)
                    self.screen.blit(image, (col * self.settings.cellSize[0] + self.settings.boardOffset[0], row * self.settings.cellSize[1] + self.settings.boardOffset[1]))

    def draw_captured_pieces(self):
        self.capturedPieces[0] = sorted(self.capturedPieces[0])
        self.capturedPieces[1] = sorted(self.capturedPieces[1])
        score = 0
        for i in range(len(self.capturedPieces[0])):
            image = pygame.image.load(self.settings.piecesImages[self.capturedPieces[0][i]]).convert_alpha()
            image = pygame.transform.scale(image, self.settings.smallPieceIcon)
            self.screen.blit(image, (i * self.settings.smallPieceIcon[0] * self.settings.capturePieceDist, self.settings.boardSize[1] + self.settings.boardOffset[1]))
            score += self.settings.pieceScore[self.capturedPieces[0][i]]
        
        for i in range(len(self.capturedPieces[1])):
            image = pygame.image.load(self.settings.piecesImages[self.capturedPieces[1][i]]).convert_alpha()
            image = pygame.transform.scale(image, self.settings.smallPieceIcon)
            self.screen.blit(image, (i * self.settings.smallPieceIcon[0] * self.settings.capturePieceDist, self.settings.boardOffset[1] // 2))
            score -= self.settings.pieceScore[self.capturedPieces[1][i]]
        # print(score)
        if(score > 0):
            font = pygame.font.Font(None, 36)
            text = font.render("+" + str(abs(score)), True, (0, 0, 0))
            self.screen.blit(text, (self.settings.smallPieceIcon[0] * self.settings.capturePieceDist * (len(self.capturedPieces[0]) + 1), self.settings.boardSize[1] + self.settings.boardOffset[1] * 5 // 4))

        if(score < 0):
            font = pygame.font.Font(None, 36)
            text = font.render("+" + str(abs(score)), True, (0, 0, 0))
            self.screen.blit(text, (self.settings.smallPieceIcon[0] * self.settings.capturePieceDist * (len(self.capturedPieces[1]) + 1), self.settings.boardOffset[1] * 3 // 4))
    
    def draw_checkmate(self):
        font = pygame.font.Font(None, 36)
        text = font.render("CHECKMATE", True, (0, 0, 0))
        self.screen.blit(text, (self.settings.boardSize[0] // 2, self.settings.boardSize[1] // 2))

    def update_screen(self):
        self.screen.fill(self.settings.bgcolor)
        self.draw_board()
        if self.checkmated:
            self.draw_checkmate()
        self.draw_captured_pieces()
        pygame.display.flip()

    def run(self):
        while True:
            self.check_event()
            self.update_screen()

game = Chess("CHESS")
game.run()