class Square:
    def __init__(self,row,col,piece=None) -> None:
        self.row=row
        self.col=col
        self.piece=piece
        
    def __eq__(self, other) -> bool:
        if self.row==other.row  and self.col==other.col:
            return True
        else:
            return False
    def is_empty(self):
        if self.piece is None:
            return True
        else:
            return False
    @staticmethod
    def is_inside_board(r,c):
        if 0<=r<=7 and 0<=c<=7:
            return True
        else:
            return False
    def is_enemy(self,color):
        if not self.is_empty() and self.piece.color!= color:
            return True
        else:
            return False

        
