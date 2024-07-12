import pygame as py
from CONSTS import *
from render import Render
import sys
from click import Drag
from board import Board
from morabae import Square
from move import Move


class Main:
    def __init__(self) -> None:
        py.init()
        self.screen=py.display.set_mode((WIDTH,HEIGHT)) #creating a pygame screen
        self.srfc=py.Surface((WIDTH,HEIGHT),py.SRCALPHA)
        
        py.display.set_caption('chess')
        self.game=Render()
        self.drag=Drag()
        self.board=Board()

    def game_loop(self):
        while True:
            self.game.display_grid(self.screen)
            self.game.display_possible_moves(self.screen,self.drag.moved,self.drag.piece)
            self.game.display_pieces(self.screen,self.board)

            if self.drag.moved:
                self.drag.show_dragging_motion(self.screen)
                
            for event in py.event.get():
                #the order is : click_move_release 
                if event.type==py.MOUSEBUTTONDOWN:
                    self.drag.update_mouse_pos(event.pos)
                    clicked_r=self.drag.y_mouse // CELL_SIZE
                    clicked_c=self.drag.x_mouse //CELL_SIZE
                    
                    if not self.board.cells[clicked_r][clicked_c].is_empty():
                        p=self.board.cells[clicked_r][clicked_c].piece

                        #check to see if the right player is moving its pieces
                        if p.color== self.game.player_turn:

                            self.board.calculate_moves(p,clicked_r,clicked_c,calc_key=True)
                            self.drag.save_initital_piece((clicked_r,clicked_c))
                            self.drag.the_piece(p) #saving the piece
                        
                            self.game.display_grid(self.screen)
                            self.game.display_possible_moves(self.screen,self.drag.moved,self.drag.piece)
                            self.game.display_pieces(self.screen,self.board)

                elif event.type==py.MOUSEMOTION:
                    if self.drag.moved:
                       
                        self.drag.update_mouse_pos(event.pos)
                        self.game.display_grid(self.screen)
                        self.game.display_possible_moves(self.screen,self.drag.moved,self.drag.piece)
                        self.game.display_pieces(self.screen,self.board)
                        self.drag.show_dragging_motion(self.screen)

                    
                elif event.type==py.MOUSEBUTTONUP:
                    if self.drag.moved:
                        self.drag.update_mouse_pos(event.pos)
                        dest_row,dest_col=self.drag.y_mouse//CELL_SIZE , self.drag.x_mouse//CELL_SIZE

                        start_sqr=Square(self.drag.start_row,self.drag.start_col)
                        dest_sqr=Square(dest_row,dest_col)
                        temp_move=Move(start_sqr,dest_sqr)
                        #is it a valid move
                        if self.board.is_a_valid_move(self.drag.piece,temp_move):

                            #check pawn promotion

                            self.board.move_the_piece(self.drag.piece,temp_move)

                            if self.board.check_pawn_promotion(self.drag.piece,dest_sqr):
                                #display the promotion menu
                                inputt=self.game.draw_promotion_input(self.screen,self.srfc)
                                self.board.place_pawn_promotion(inputt,dest_sqr,self.drag.piece.color)


                            self.board.en_passant_boolian_checker(self.drag.piece)
                            self.game.display_pieces(self.screen,self.board)
                            #change the turns
                            self.game.turn_changer() 
                            #winner yet?
                            if self.board.winner_yet(self.game.player_turn):
                                return 
                    self.drag.undrag_piece()

                elif event.type== py.QUIT:
                    py.quit()
                    sys.exit()
            
            py.display.update()
            
main=Main()
main.game_loop()
main.game.display_winner()

#2024
