import os
from morabae import Square

class Piece:
    def __init__(self,name,color,img=None,img_rect=None) -> None:
        self.name=name
        self.color=color
        self.img=img
        self.set_img()
        self.img_rect=img_rect
        self.valid_moves=[]
        self.has_moved=False

    def set_img(self):
        self.img = os.path.join(
            f'green_set/{self.name.lower()}_{self.color.lower()}.png')   
          
    def add_valid_move(self,move):
        self.valid_moves.append(move)
    
    def clear_moves(self):
        self.valid_moves=[]
    

# diffrent piece classes:
        
class King(Piece):
    def __init__(self,color) -> None:
        super().__init__('King',color)
        self.castel_left=None
        self.castel_right=None
        
    def possible_moves(self,row,col):
        moves=[]
        offsets=[(1, 0), (0, 1), (-1, 0), (0, -1),
                (1, 1), (-1, 1), (1, -1), (-1, -1)]
        for r , c in offsets:
            new_row,new_col=(row+r,col+c)
            moves.append((new_row,new_col))
        return moves
            

class Queen(Piece):
    def __init__(self,color) -> None:
        super().__init__('Queen',color)

    def possible_moves(self,row,col):
        increasments=[(1,-1),(1,1),(-1,-1),(-1,1),(1,0),(0,1),(-1,0),(0,-1)]
        lst=[[],[],[],[],[],[],[],[]]
        for i, (dr,dc) in enumerate(increasments):
            new_row,new_col=(row+dr,col+dc)
            while 0<=new_row<=7 and 0<=new_col<=7:
                lst[i].append((new_row,new_col))
                new_row+=dr
                new_col+=dc
        return lst

class Bishop(Piece):
    def __init__(self,color) -> None:
        super().__init__('Bishop',color)

    def possible_moves(self,row,col):
        increasments=[(1,-1),(1,1),(-1,-1),(-1,1)]
        lst=[[],[],[],[]]
        for i, (dr,dc) in enumerate(increasments):
            new_row,new_col=(row+dr,col+dc)
            while 0<=new_row<=7 and 0<=new_col<=7:
                lst[i].append((new_row,new_col))
                new_row+=dr
                new_col+=dc
        return lst

class Rook(Piece):
    def __init__(self,color) -> None:
        super().__init__('Rook',color)

    def possible_moves(self,row,col):
        increasments=[(1,0),(0,1),(-1,0),(0,-1)]
        lst=[[],[],[],[]]
        for i, (dr,dc) in enumerate(increasments):
            new_row,new_col=(row+dr,col+dc)
            while 0<=new_row<=7 and 0<=new_col<=7:
                lst[i].append((new_row,new_col))
                new_row+=dr
                new_col+=dc
        return lst
            
class Knight(Piece):
    def __init__(self,color) -> None:
        super().__init__('Knight',color)

    def possible_moves(self,row,col):
        offsets=[(-2,1),(-1,2),(1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1)]
        all_moves=[]
        for r,c in offsets:
            new_row,new_col=(row+r,col+c)
            all_moves.append((new_row,new_col))
        
        return all_moves

class Pawn(Piece):
    def __init__(self,color) -> None:
        super().__init__('Pawn',color)
        self.enpassant=False
        
    def possible_moves(self,row,col):
        starter=False
        all_moves=[]
        capture_move=[]
        common=[-1,+1]
        d=1 if self.color=='Black' else -1
        start_row = 1 if self.color == "Black" else 6

        new_move=(row+d,col)
        all_moves.append(new_move)

        for dc in common:
            new_move=(row+d,col+dc)
            capture_move.append(new_move)
        #the can jump 2 rule
        if start_row == row:
            starter=True

        return (all_moves,capture_move,starter)


    