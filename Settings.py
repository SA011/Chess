class Settings:
    def __init__(self):
        self.boardSize = (800, 800)
        self.screen = (800, 1000)
        self.bgcolor = (200, 200, 200)

        self.cellSize = (self.boardSize[0] / 8, self.boardSize[1] / 8)
        self.cellColorWhite = (255, 255, 255)
        self.cellColorBlack = (100, 100, 100)
        self.boardOffset = (0, 100)
        self.smallPieceIcon = (50, 50)
        self.selectedColorChange = (-100, -100, 0)
        self.moveColorChange = (-40, -40, 0)
        self.capturePieceDist = 0.45

        self.menuSize = (400, 700)
        self.menuOffset = (200, 100)
        self.menuColor = (100, 100, 100)
        self.menuTextColor = (255, 255, 255)
        self.menuButtonSize = (200, 50)
        self.menuButtonColor = (50, 50, 50)
        self.menuButtonTextColor = (255, 255, 255)
        self.menuButtonOffset = (100, 50)

        self.resultScreenSize = (400, 400)
        self.resultScreenOffset = (200, 400)
        self.resultScreenColor = (100, 100, 100)
        self.resultScreenTextColor = (255, 255, 255)
        self.resultScreenButtonSize = (200, 50)
        self.resultScreenButtonColor = (50, 50, 50)
        self.resultScreenButtonTextColor = (255, 255, 255)
        self.resultScreenButtonOffset = (100, 50)

        self.inputBoxSize = (400, 50)
        self.inputBoxOffset = (200, 100)
        self.inputBoxColor = (255, 255, 255)
        self.inputBoxTextColor = (0, 0, 0)
        self.inputBoxButtonSize = (200, 50)
        self.inputBoxButtonColor = (50, 50, 50)
        self.inputBoxButtonDisabledColor = (100, 100, 100)
        self.inputBoxButtonTextColor = (255, 255, 255)
        self.inputBoxButtonOffset = (100, 50)



        self.piecesImages = {
            "PAWN": "images/white_pawn.png",
            "ROOK": "images/white_rook.png",
            "KNIGHT": "images/white_knight.png",
            "BISHOP": "images/white_bishop.png",
            "QUEEN": "images/white_queen.png",
            "KING": "images/white_king.png",
            "pawn": "images/black_pawn.png",
            "rook": "images/black_rook.png",
            "knight": "images/black_knight.png",
            "bishop": "images/black_bishop.png",
            "queen": "images/black_queen.png",
            "king": "images/black_king.png"
        }

        self.pieceScore = {
            "Pawn": 100,
            "Rook": 500,
            "Knight": 300,
            "Bishop": 300,
            "Queen": 900,
            "King": 10000
        }

        self.BLACK = 1
        self.WHITE = 0


    def checkPosition(self, position):
        return position[0] >= 0 and position[0] < 8 and position[1] >= 0 and position[1] < 8





