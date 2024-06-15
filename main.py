import pygame
import Settings
from Chess import Chess
from Piece import *
from Move import *
import random
from MinMax import *
from AlphaBeta import *

class Game:
    def __init__(self, caption):
        self.DEPTH = 2
        pygame.init()
        self.settings = Settings.Settings()
        self.caption = caption
        self.screen = pygame.display.set_mode(self.settings.screen)
        pygame.display.set_caption(caption)
        
        self.game = Chess()
        self.selected = [[0 for i in range(8)] for j in range(8)]
        self.selectedPiece = (0, 0)
        self.automated = [False, True]
        
        self.mainmenu = True
        self.resultScreen = False
        self.result = None
        # self.lichess = None
        # self.inputbox = ""
    
    def new_game(self):
        self.game = Chess()
        self.selected = [[0 for i in range(8)] for j in range(8)]
        self.selectedPiece = (0, 0)


    # def initLicess(self):
    #     pass
    def check_event(self):
        if not self.mainmenu and not self.resultScreen:# and self.lichess == None:
            if self.game.checkIfCheckMate():
                self.result = 1 - self.game.turn
                self.resultScreen = True
                return
            elif self.game.checkIfStaleMate():
                self.result = None
                self.resultScreen = True
            elif self.automated[self.game.turn]:
                # ai = MinMax(self.game, self.DEPTH)
                ai = AlphaBeta(self.game, self.DEPTH)
                move = ai.getBestMove()
                # print(ai.explored)
                if move:
                    self.game.move(move)
                    # print(ai.bestScore)
    

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
            # if event.type == pygame.KEYDOWN:
            #     if self.lichess == "":
            #         if event.key == pygame.K_BACKSPACE:
            #             if self.inputbox != "":
            #                 self.inputbox = self.inputbox[:-1]
            #         elif event.key == pygame.K_RETURN:
            #             if self.inputbox == "":
            #                 continue
            #             self.lichess = self.inputbox
            #             self.initLicess()
            #         else:
            #             self.inputbox += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.mainmenu:
                    x, y = pygame.mouse.get_pos()
                    if x >= self.settings.menuOffset[0] + self.settings.menuButtonOffset[0] and x <= self.settings.menuOffset[0] + self.settings.menuButtonOffset[0] + self.settings.menuButtonSize[0] and y >= self.settings.menuOffset[1] and y <= self.settings.menuOffset[1] + self.settings.menuSize[1]:
                        x -= self.settings.menuOffset[0]
                        y -= self.settings.menuOffset[1]
                        y = int(y / self.settings.menuButtonOffset[1])
                        if y % 2 == 0:
                            continue
                        y = y // 2
                        if y == 0:
                            self.automated = [False, False]
                            self.new_game()
                            self.mainmenu = False
                        elif y == 1:
                            self.automated = [False, True]
                            self.new_game()
                            self.mainmenu = False
                        elif y == 2:
                            self.automated = [True, False]
                            self.new_game()
                            self.mainmenu = False
                        elif y == 3:
                            self.automated = [True, True]
                            self.new_game()
                            self.mainmenu = False
                        elif y == 4:
                            exit(0)
                        # elif y == 4:
                        #     self.lichess = self.inputbox = ""
                        #     self.mainmenu = False
                    continue

                if self.resultScreen:
                    x, y = pygame.mouse.get_pos()
                    if x >= self.settings.resultScreenOffset[0] + self.settings.resultScreenButtonOffset[0] and x <= self.settings.resultScreenOffset[0] + self.settings.resultScreenButtonOffset[0] + self.settings.resultScreenButtonSize[0] and y >= self.settings.resultScreenOffset[1] and y <= self.settings.resultScreenOffset[1] + self.settings.resultScreenSize[1]:
                        y -= self.settings.resultScreenOffset[1]
                        y = int(y / self.settings.resultScreenButtonOffset[1])
                        if y % 2 == 0:
                            continue
                        y = y // 2
                        if y == 1:
                            self.mainmenu = True
                            self.resultScreen = False
                        elif y == 2:
                            exit(0)
                    continue
                # if self.lichess != None:
                #     continue
                # print(self.game.Kings[0].position, self.game.Kings[1].position)
                c, r = pygame.mouse.get_pos()
                c -= self.settings.boardOffset[0]
                r -= self.settings.boardOffset[1]
                c = int(c / self.settings.cellSize[0])
                r = 7 - int(r / self.settings.cellSize[1])
                if not self.settings.checkPosition((r, c)):
                    self.selected = [[0 for i in range(8)] for j in range(8)]
                    self.selectedPiece = None    
                    continue
                if self.automated[self.game.turn]:
                    continue
                if self.selected[r][c] == 2:
                    for move in self.moves:
                        if move.to_square.position == (r, c):
                            self.game.move(move)
                            break
                    self.selected = [[0 for i in range(8)] for j in range(8)]
                else:
                    self.selected = [[0 for i in range(8)] for j in range(8)]
                    self.selectedPiece = self.game.getPiece((r, c))
                    self.moves = self.game.getMoves(self.selectedPiece, checkCheck=True)
                    for move in self.moves:
                        self.selected[move.to_square.position[0]][move.to_square.position[1]] = 2
                    self.selected[r][c] = 1
    def draw_board(self):
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 != 0:
                    color = self.settings.cellColorWhite
                else:
                    color = self.settings.cellColorBlack
                
                if self.selected[row][col] == 1:
                    # slight bluish color on top of the cell
                    color = (color[0] + self.settings.selectedColorChange[0], color[1] + self.settings.selectedColorChange[1], color[2] + self.settings.selectedColorChange[2])
                if self.selected[row][col] == 2:
                    # slight greenish color on top of the cell
                    color = (color[0] + self.settings.moveColorChange[0], color[1] + self.settings.moveColorChange[1], color[2] + self.settings.moveColorChange[2])
                
                pygame.draw.rect(self.screen, color, (col * self.settings.cellSize[0] + self.settings.boardOffset[0], (7 - row) * self.settings.cellSize[1] + self.settings.boardOffset[1], self.settings.cellSize[0], self.settings.cellSize[1]))

                piece = self.game.getPiece((row, col))
                if piece.__class__.__name__ != "Empty":
                    image = pygame.image.load(piece.image).convert_alpha()
                    image = pygame.transform.scale(image, self.settings.cellSize)
                    self.screen.blit(image, (col * self.settings.cellSize[0] + self.settings.boardOffset[0], (7 - row) * self.settings.cellSize[1] + self.settings.boardOffset[1]))
    
    def drawMainMenu(self):
        # draw menu with 5 buttons - 2 Player, Play as Black, Play as White, Automate, Exit
        # buttons should be centered and should be clickable

        # draw menu background
        pygame.draw.rect(self.screen, self.settings.menuColor, (self.settings.menuOffset[0], self.settings.menuOffset[1], self.settings.menuSize[0], self.settings.menuSize[1]))
        # draw menu buttons
        buttons = ["      2 Player", "  Play as White", "  Play as Black", "     Automate","          Exit"]
        for i, button in enumerate(buttons):
            pygame.draw.rect(self.screen, self.settings.menuButtonColor, (self.settings.menuOffset[0] + self.settings.menuButtonOffset[0], self.settings.menuOffset[1] + (2 * i + 1) * self.settings.menuButtonOffset[1], self.settings.menuButtonSize[0], self.settings.menuButtonSize[1]))
            font = pygame.font.Font(None, 36)
            text = font.render(button, True, self.settings.menuButtonTextColor)
            self.screen.blit(text, (self.settings.menuOffset[0] + self.settings.menuButtonOffset[0] + 10, self.settings.menuOffset[1] + (2 * i + 1) * self.settings.menuButtonOffset[1] + 10))
    
    def drawResultScreen(self):
        # draw result screen with 2 buttons - Play Again, Exit
        # buttons should be centered and should be clickable

        # draw result screen background
        pygame.draw.rect(self.screen, self.settings.resultScreenColor, (self.settings.resultScreenOffset[0], self.settings.resultScreenOffset[1], self.settings.resultScreenSize[0], self.settings.resultScreenSize[1]))
        # draw result screen buttons
        buttons = ["     Play Again", "         Exit"]
        result = "      DRAW"
        if self.result == self.settings.WHITE:
            result = "WHITE WINS"
        elif self.result == self.settings.BLACK:
            result = "BLACK WINS"
        font = pygame.font.Font(None, 50)
        text = font.render(result, True, self.settings.resultScreenTextColor)
        self.screen.blit(text, (self.settings.resultScreenOffset[0] + self.settings.resultScreenButtonOffset[0] - 5, self.settings.resultScreenOffset[1] + self.settings.resultScreenButtonOffset[1]))

        for i, button in enumerate(buttons):
            pygame.draw.rect(self.screen, self.settings.resultScreenButtonColor, (self.settings.resultScreenOffset[0] + self.settings.resultScreenButtonOffset[0], self.settings.resultScreenOffset[1] + (2 * i + 3) * self.settings.resultScreenButtonOffset[1], self.settings.resultScreenButtonSize[0], self.settings.resultScreenButtonSize[1]))
            font = pygame.font.Font(None, 36)
            text = font.render(button, True, self.settings.resultScreenButtonTextColor)
            self.screen.blit(text, (self.settings.resultScreenOffset[0] + self.settings.resultScreenButtonOffset[0] + 10, self.settings.resultScreenOffset[1] + (2 * i + 3) * self.settings.resultScreenButtonOffset[1] + 10))
    # def draw_lichess(self):
    #     if self.lichess == "":
    #         #input box will take an string input
    #         # draw input box background
    #         pygame.draw.rect(self.screen, self.settings.inputBoxColor, (self.settings.inputBoxOffset[0], self.settings.inputBoxOffset[1], self.settings.inputBoxSize[0], self.settings.inputBoxSize[1]))
    #         # draw input box text
    #         font = pygame.font.Font(None, 36)
    #         text = font.render("Enter Lichess Game ID", True, self.settings.inputBoxTextColor)
    #         self.screen.blit(text, (self.settings.inputBoxOffset[0] + 10, self.settings.inputBoxOffset[1] - 30))
            
    #         font = pygame.font.Font(None, 30)
    #         text = font.render(self.inputbox, True, self.settings.inputBoxTextColor)
    #         self.screen.blit(text, (self.settings.inputBoxOffset[0] + 10, self.settings.inputBoxOffset[1] - 30))
            
    #         # draw input box buttons
    #         buttons = ["       Submit", "         Back"]
    #         for i, button in enumerate(buttons):
    #             pygame.draw.rect(self.screen, self.settings.inputBoxButtonColor, (self.settings.inputBoxOffset[0] + self.settings.inputBoxButtonOffset[0], self.settings.inputBoxOffset[1] + (2 * i + 2) * self.settings.inputBoxButtonOffset[1], self.settings.inputBoxButtonSize[0], self.settings.inputBoxButtonSize[1]))
    #             font = pygame.font.Font(None, 36)
    #             text = font.render(button, True, self.settings.inputBoxButtonTextColor)
    #             self.screen.blit(text, (self.settings.inputBoxOffset[0] + self.settings.inputBoxButtonOffset[0] + 10, self.settings.inputBoxOffset[1] + (2 * i + 2) * self.settings.inputBoxButtonOffset[1] + 10))
    
    def update_screen(self):
        self.screen.fill(self.settings.bgcolor)
        if self.mainmenu:
            self.drawMainMenu()
        elif self.resultScreen:
            self.draw_board()
            self.drawResultScreen()
        # elif self.lichess != None:
        #     self.draw_lichess()
        else:
            self.draw_board()
        pygame.display.flip()

    def run(self):
        while True:
            self.check_event()
            self.update_screen()

game = Game("CHESS")
game.run()