from CONSTS import * 
from morabae import Square
from piece import *
from move import Move
# 
import pdb
import copy

class Board:
    def __init__(self) -> None:
        self.cells=[[None,None,None,None,None,None,None,None]
                    ,[None,None,None,None,None,None,None,None]
                    ,[None,None,None,None,None,None,None,None]
                    ,[None,None,None,None,None,None,None,None]
                    ,[None,None,None,None,None,None,None,None]
                    ,[None,None,None,None,None,None,None,None]
                    ,[None,None,None,None,None,None,None,None]
                    ,[None,None,None,None,None,None,None,None]]

        for r in range(ROWS):
            for c in range(COLS):
                self.cells[r][c]=Square(r,c)
           
        self.place_piece("White")
        self.place_piece('Black')

        self.promotion_screen=False

    def place_piece(self,color):
        pawn_row,main_row=[6,7] if color=="White" else [1,0]
        #pawns
        for j in range(COLS):
            self.cells[pawn_row][j]=Square(pawn_row,j,Pawn(color))
        #other pieces
        self.cells[main_row][0]=Square(main_row,0,Rook(color))
        self.cells[main_row][7]=Square(main_row,7,Rook(color))

        self.cells[main_row][1]=Square(main_row,1,Knight(color))
        self.cells[main_row][6]=Square(main_row,6,Knight(color))

        self.cells[main_row][2]=Square(main_row,2,Bishop(color))
        self.cells[main_row][5]=Square(main_row,5,Bishop(color))

        self.cells[main_row][3]=Square(main_row,3,Queen(color))
        self.cells[main_row][4]=Square(main_row,4,King(color))
    
    def move_the_piece(self,piece,move,check_pass=False):
        start=move.start #its a square
        dest=move.dest   #its a square
        empty=self.cells[dest.row][dest.col].is_empty() # true or false

        self.cells[start.row][start.col].piece= None #empty the current cell
        self.cells[dest.row][dest.col].piece= piece #place the piece

        self.check_pawn_promotion(piece,dest)
        self.king_casteling(piece,start,dest,check_pass)
        self.pawn_en_passant_move(piece,start,dest,empty)

        piece.has_moved=True

        piece.clear_moves() # bcz were done/ we moved the picece and dont need thos positions

    def is_a_valid_move(self,piece,move):
        if move in piece.valid_moves:
            return True
        else:
            return False
    def en_passant_boolian_checker(self,piece):
        ''' if its a pawn, set all pawns to false and then set the one that we have just moves to true
            if its not then set all of them to false
        '''
        if isinstance(piece,Pawn):
            for row in range(ROWS):
                for col in range(COLS):
                    if not self.cells[row][col].is_empty():
                        self.cells[row][col].piece.enpassant=False
            piece.enpassant=True
        else:
            for row in range(ROWS):
                for col in range(COLS):
                    if isinstance(self.cells[row][col].piece,Pawn):
                        self.cells[row][col].piece.enpassant=False

    def pawn_en_passant_move(self,piece,start,dest,empty):
        if isinstance(piece,Pawn):
            delta=(dest.col - start.col)
            if delta !=0 and empty:
                self.cells[start.row][start.col + delta ].piece=None
                self.cells[dest.row][dest.col].piece= piece

    def king_casteling(self,piece,start,dest,check_pass):
        #we dont want this to run when the check function uses the move method
        if isinstance(piece,King) and not check_pass:
            dif=(start.col - dest.col)
            if abs(dif)==2:
                #means we have to castel now
                # right or left casteling?
                if dif < 0 :
                    #right casteling :
                    rightrook=piece.castel_right
                    self.move_the_piece(rightrook,rightrook.valid_moves[-1])
                else:
                    rook=piece.castel_left
                    self.move_the_piece(rook,rook.valid_moves[-1])

    def is_in_check(self,piece,move):
        tmp_board=copy.deepcopy(self)
        tmp_piece=copy.deepcopy(piece)

        tmp_board.move_the_piece(tmp_piece,move,True)

        for row in range(ROWS):
            for col in range(COLS):
                if tmp_board.cells[row][col].is_enemy(piece.color):
                    p=tmp_board.cells[row][col].piece
                    tmp_board.calculate_moves(p,row,col,calc_key=False)
                    for i in p.valid_moves:
                        if isinstance(i.dest.piece,King):
                            p.clear_moves()
                            return True
        p.clear_moves()
        return False
    
    def winner_yet(self,color):
        for row in range(ROWS):
            for col in range(COLS):
                piece=self.cells[row][col].piece
                if not self.cells[row][col].is_empty():
                    if not self.cells[row][col].is_enemy(color):
                        self.calculate_moves(piece,row,col,True)
                        if len(piece.valid_moves)>=1:
                            return False
        return True

    def check_pawn_promotion(self,piece,dest):
        if isinstance(piece,Pawn):
            if dest.row==0 or dest.row==7:
                #set up the menu screen
                self.promotion_screen=True
                return True
                #self.cells[dest.row][dest.col].piece= Queen(piece.color)

    def place_pawn_promotion(self,choosen_piece,dest,colour):

        if choosen_piece=='q':
            self.cells[dest.row][dest.col].piece= Queen(colour)

        elif choosen_piece=='r':
            self.cells[dest.row][dest.col].piece= Rook(colour)

        elif choosen_piece=='b':
            self.cells[dest.row][dest.col].piece= Bishop(colour)

        elif choosen_piece=='k':
            self.cells[dest.row][dest.col].piece= Knight(colour)


    

    def calculate_moves(self,piece,row,col,calc_key):


        def valid_knight_moves():
            piece.clear_moves()
            allMoves=piece.possible_moves(row,col)
            for move in allMoves:
                move_row,move_col=move
                if Square.is_inside_board(move_row,move_col):
                    if self.cells[move_row][move_col].is_empty() or self.cells[move_row][move_col].is_enemy(piece.color):
                        
                        enemy_piece=self.cells[move_row][move_col].piece # passing the enemy piece to the dest sqr to see if its check
                        move=Move(Square(row,col),Square(move_row,move_col,enemy_piece))
                        if calc_key:
                            if not self.is_in_check(piece,move):
                                piece.add_valid_move(move)
                            else:
                                continue
                        else:
                            piece.add_valid_move(move)
                        
        def valid_pawn_moves():
            piece.clear_moves()
            key=False
            d=1 if piece.color=='Black' else -1
            allMoves,captureMoves,starter=piece.possible_moves(row,col)
            
            for move in allMoves:
                move_row,move_col=move
                if Square.is_inside_board(move_row,move_col):
                    if self.cells[move_row][move_col].is_empty():

                        enemy_piece=self.cells[move_row][move_col].piece
                        move1=Move(Square(row,col),Square(move_row,move_col,enemy_piece))
                        if calc_key:
                            if not self.is_in_check(piece,move1):
                                key=True
                                piece.add_valid_move(move1)
                            else:
                                key=False
                                break
                        else:
                            key=True
                            piece.add_valid_move(move1)

            for cMove in captureMoves:
                move_row,move_col=cMove
                if Square.is_inside_board(move_row,move_col):
                    if self.cells[move_row][move_col].is_enemy(piece.color)==True and self.cells[move_row][move_col].is_empty()==False:
                       
                        enemy_piece=self.cells[move_row][move_col].piece
                        #diagonal moves are also valid
                        move=Move(Square(row,col),Square(move_row,move_col,enemy_piece))
                        if calc_key:
                            if not self.is_in_check(piece,move):
                                
                                piece.add_valid_move(move)
                            else:
                                continue
                        else:
                            piece.add_valid_move(move)
                      
            #check the 2 forward rule:
            if starter and key:
                new_move=(row+d+d,col)
                move_row,move_col=new_move

                if Square.is_inside_board(move_row,move_col):
                    if self.cells[move_row][move_col].is_empty(): 
                        enemy_piece=self.cells[move_row][move_col].piece
                        move=Move(Square(row,col),Square(move_row,move_col,enemy_piece))
                        if calc_key:
                            if not self.is_in_check(piece,move):
                                piece.add_valid_move(move)
                        else:
                            piece.add_valid_move(move)

            #en passant moves:
            en_row=3 if piece.color=='White' else 4
            dest_row=2 if piece.color=='White' else 5
            if row==en_row:
            #right side:
                if 0<=(col+1)<=7:
                    if not self.cells[row][col+1].is_empty() and self.cells[row][col+1].is_enemy(piece.color):
                
                       right_enemy_pawn=self.cells[row][col+1].piece
                       if isinstance(right_enemy_pawn,Pawn):
                           if right_enemy_pawn.enpassant:
                               #means it has just moved
                               en_start=Square(row,col)
                               en_dest=Square(dest_row,col+1)
                               en_move=Move(en_start,en_dest)
                               #check if its in check
                               if calc_key:
                                    if not self.is_in_check(piece,en_move):
                                        piece.add_valid_move(en_move)
                               else:
                                   piece.add_valid_move(en_move)
            #left side:
                if 0<=(col-1)<=7:
                    if not self.cells[row][col-1].is_empty() and self.cells[row][col-1].is_enemy(piece.color):
                       left_enemy_pawn=self.cells[row][col-1].piece
                       if isinstance(left_enemy_pawn,Pawn):
                           if left_enemy_pawn.enpassant:
                               #means it has just moved
                               en_start=Square(row,col)
                               en_dest=Square(dest_row,col-1)
                               en_move=Move(en_start,en_dest)
                               #check if its in check
                               if calc_key:
                                    if not self.is_in_check(piece,en_move):
                                        piece.add_valid_move(en_move)
                               else:
                                   piece.add_valid_move(en_move)
                    
        def valid_rook_moves():
            piece.clear_moves()
            allMoves=piece.possible_moves(row,col)
            for lst in allMoves:
                for move_row,move_col in lst:
                    if Square.is_inside_board(move_row,move_col):
                    # must pass this if all the time
                        if self.cells[move_row][move_col].is_empty():
                            move=Move(Square(row,col),Square(move_row,move_col))
                            if calc_key:
                                if not self.is_in_check(piece,move):
                                    piece.add_valid_move(move)
                                else:
                                    continue
                            else:
                                piece.add_valid_move(move)
                        
                        elif not self.cells[move_row][move_col].is_empty() and not self.cells[move_row][move_col].is_enemy(piece.color):
                            #blocked by its own team piece
                            break

                        elif self.cells[move_row][move_col].is_enemy(piece.color):
                            enemy_piece=self.cells[move_row][move_col].piece # passing the enemy piece to the dest sqr to see if its check
                            move=Move(Square(row,col),Square(move_row,move_col,enemy_piece))

                            if calc_key:
                                if not self.is_in_check(piece,move):
                                    piece.add_valid_move(move)
                                else:
                                    break
                            else:
                                piece.add_valid_move(move)
                            break
                            #move to the next list of moves
        
        def check_check(current_list):
            '''this function is only used when squares are empty and king in check'''
            k=False
            move_list=[]
            for move in current_list:
                move_r,move_c=move
                if Square.is_inside_board(move_r,move_c):

                    if self.cells[move_r][move_c].is_empty():
                            m=Move(Square(row,col),Square(move_r,move_c))
                            if calc_key:
                                if not self.is_in_check(piece,m):
                                    move_list.append(m)
                                else:
                                    continue
                            else:
                                move_list.append(m)

        def valid_bishop_moves():
            piece.clear_moves()
            allMoves=piece.possible_moves(row,col)
            for lst in allMoves:
                for move_row,move_col in lst:
                    if Square.is_inside_board(move_row,move_col):
                     # must pass this if all the time
                        if self.cells[move_row][move_col].is_empty():
                            move=Move(Square(row,col),Square(move_row,move_col))
                            if calc_key:
                                if not self.is_in_check(piece,move):
                                    piece.add_valid_move(move)
                                else:
                                    continue
                            else:
                                piece.add_valid_move(move)
                    
                        elif not self.cells[move_row][move_col].is_empty() and not self.cells[move_row][move_col].is_enemy(piece.color):
                            #blocked by its own team piece
                            break

                        elif self.cells[move_row][move_col].is_enemy(piece.color):
                            enemy_piece=self.cells[move_row][move_col].piece
                            move=Move(Square(row,col),Square(move_row,move_col,enemy_piece))
                            if calc_key:
                                if not self.is_in_check(piece,move):
                                    piece.add_valid_move(move)
                                else:
                                    break
                            else:
                                piece.add_valid_move(move)
                            break

        def valid_queen_moves():
            piece.clear_moves()
            allMoves=piece.possible_moves(row,col)
            for lst in allMoves:
                for move_row,move_col in lst:
                    if Square.is_inside_board(move_row,move_col):
                    # must pass this if all the time
                        if self.cells[move_row][move_col].is_empty():
                            move=Move(Square(row,col),Square(move_row,move_col))
                            if calc_key:
                                if not self.is_in_check(piece,move):
                                    piece.add_valid_move(move)
                                else:
                                    continue
                            else:
                                piece.add_valid_move(move)
    
                        elif not self.cells[move_row][move_col].is_empty() and not self.cells[move_row][move_col].is_enemy(piece.color):
                            #blocked by its own team piece
                            break

                        elif self.cells[move_row][move_col].is_enemy(piece.color):
                            enemy_piece=self.cells[move_row][move_col].piece
                            move=Move(Square(row,col),Square(move_row,move_col,enemy_piece))
                            if calc_key:
                                if not self.is_in_check(piece,move):
                                    piece.add_valid_move(move)
                            else:
                                piece.add_valid_move(move)
                            break

        def valid_king_moves():
            piece.clear_moves()
            allMoves=piece.possible_moves(row,col)
            for move in allMoves:
                move_row,move_col=move
                if Square.is_inside_board(move_row,move_col):
                    if self.cells[move_row][move_col].is_empty() or self.cells[move_row][move_col].is_enemy(piece.color):
                        enemy_piece=self.cells[move_row][move_col].piece

                        move=Move(Square(row,col),Square(move_row,move_col,enemy_piece))
                        if calc_key:
                            if not self.is_in_check(piece,move):
                                piece.add_valid_move(move)
                            else:
                                continue
                        else:
                            piece.add_valid_move(move)

            #casteling moves:                
            if piece.has_moved==False:
                #right
                right_rook=self.cells[row][7].piece
                if isinstance(right_rook,Rook):
                    if right_rook.has_moved==False:
                        if self.cells[row][6].is_empty() and self.cells[row][5].is_empty():
                            piece.castel_right=right_rook #saving cuz we have to move this too
                            
                            #rook move:
                            right_rook_move_start=Square(row,7)
                            right_rook_move_dest=Square(row,5)
                            right_rook_move=Move(right_rook_move_start,right_rook_move_dest)
                            #king move:
                            r_king_move_start=Square(row,col)
                            r_king_move_dest=Square(row,6)
                            r_king_move=Move(r_king_move_start,r_king_move_dest)
                            #adding the moves to self.valid_moves
                            if calc_key:
                                if not self.is_in_check(piece,r_king_move):
                                    piece.add_valid_move(r_king_move)
                                    right_rook.add_valid_move(right_rook_move)
                #left
                left_rook=self.cells[row][0].piece
                if isinstance(left_rook,Rook):
                    if left_rook.has_moved==False:
                        if self.cells[row][1].is_empty() and self.cells[row][2].is_empty() and self.cells[row][3].is_empty():
                            piece.castel_left=left_rook #saving cuz we have to move this too
                            
                            #rook move:
                            rook_move_start=Square(row,0)
                            rook_move_dest=Square(row,3)
                            rook_move=Move(rook_move_start,rook_move_dest)
                            #king move:
                            king_move_start=Square(row,col)
                            king_move_dest=Square(row,2)
                            king_move=Move(king_move_start,king_move_dest)
                            #adding the moves to self.valid_moves
                            if calc_key:
                                if not self.is_in_check(piece,king_move):
                                    piece.add_valid_move(king_move)
                                    left_rook.add_valid_move(rook_move)

        # is instance piece:                
        if isinstance(piece,Knight):
            valid_knight_moves()
        elif isinstance(piece,Rook):
            valid_rook_moves()
        elif isinstance(piece,King):
            valid_king_moves()
        elif isinstance(piece,Bishop):
            valid_bishop_moves()
        elif isinstance(piece,Queen):
            valid_queen_moves()
        elif isinstance(piece,Pawn):
            valid_pawn_moves()

        
        
