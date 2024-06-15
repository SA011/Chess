class Move:
    def __init__(self, from_square, to_square):
        self.from_square = from_square
        self.to_square = to_square
    def copy(self):
        return Move(self.from_square.copy(), self.to_square.copy())
    
    def __str__(self):
        return f"{self.from_square} -> {self.to_square}"

class Castle(Move):
    def __init__(self, from_square, to_square, rook_from_square, rook_to_square):
        super().__init__(from_square, to_square)
        self.rook_from_square = rook_from_square
        self.rook_to_square = rook_to_square
    def copy(self):
        return Castle(self.from_square.copy(), self.to_square.copy(), self.rook_from_square.copy(), self.rook_to_square.copy())

class EnPassant(Move):
    def __init__(self, from_square, to_square, capture_square):
        super().__init__(from_square, to_square)
        self.capture_square = capture_square

    def copy(self):
        return EnPassant(self.from_square.copy(), self.to_square.copy(), self.capture_square.copy())

    def __str__(self):
        return f"{self.from_square} -> {self.to_square} (En Passant)"
