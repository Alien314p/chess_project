import pygame as py
from CONSTS import *
from board import Board
from click import Drag
import time
import sys

class Render:
    def __init__(self) -> None:
        self.player_turn='White'
       
        self.board=Board()
        self.drag=Drag()

    #display methods
    def display_grid(self,screen):
        font=py.font.Font('font/gi_incognito.ttf',15)
        for row in range(ROWS):
            for col in range(COLS):
                if (col+row)%2==0:
                    color=LIGHT_GREEN
                else:
                    color=DARK_GREEN

                sqr=(CELL_SIZE*row,CELL_SIZE*col,CELL_SIZE,CELL_SIZE)
                py.draw.rect(screen,color,sqr)
        #numbers to the grid
        alephabet=['a','b','c','d','e','f','g','h']
        for n in range(1,9):
            c=DARK_GREEN if n%2==0 else LIGHT_GREEN
            d=(n-1)*100
            screen.blit(font.render(f'{n}',True,c),(10,775-d))
    
        for a in range(8):
            c=LIGHT_GREEN if a%2==0 else DARK_GREEN
            d=(a)*100
            screen.blit(font.render(f'{alephabet[a]}',True,c),(85+d,772))



    def display_pieces(self,screen,board):
        for row in range(ROWS):
            for col in range(COLS):
                                    
                if not board.cells[row][col].is_empty():

                    p=board.cells[row][col].piece
                    if p is not self.drag.piece:
                        p.set_img()
                        image=py.image.load(p.img)
                        w=image.get_width()
                        h=image.get_height()
                        image2=py.transform.scale(image,(w*0.8, h*0.8))

                        image_pos= col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2

                        a= image_pos[0]
                        b=image_pos[1]
                        image_pos=(a+7,b+3)
                
                        p.img_rect= image.get_rect(center=image_pos)
                        screen.blit(image2,(p.img_rect))

    def display_possible_moves(self,screen,boolian,p):
       
        if boolian:
            for item in p.valid_moves:
                
                color=LIGHT_YELLOW if (item.dest.row+item.dest.col)%2==0 else DARK_YELLOW

                sqr=(CELL_SIZE*item.dest.col ,CELL_SIZE*item.dest.row,CELL_SIZE,CELL_SIZE)
                py.draw.rect(screen,color,sqr)

    def turn_changer(self):
        self.player_turn='Black' if self.player_turn=='White' else 'White'
    
    def display_winner(self):

        font=py.font.Font('font/gi_incognito.ttf',78)
        end_game_screen=py.display.set_mode((800,800))
        
        
        player='WHITE' if self.player_turn=="Black" else 'BLACK'
        text_color='BLACK' if player=='WHITE' else 'WHITE'
        
        end_game_screen.fill(player)

        text=font.render(f'{player} wins !',True,text_color)
        text_rect=text.get_rect(center=(400,400))
        while True:
            end_game_screen.blit(text,text_rect)
            for event in py.event.get():
                if event.type== py.QUIT:
                        py.quit()
                        sys.exit()
            py.display.update()
    
    def draw_promotion_input(self,screen,surface):
        font=py.font.Font('font/gi_incognito.ttf',35)
        py.draw.rect(surface,(59, 86, 138,9),[WIDTH//8,HEIGHT//8,WIDTH*3//4,HEIGHT*3//4])
        py.draw.rect(surface,'dark gray',[WIDTH*2.1//8,HEIGHT*1.5//8, WIDTH*3.75//8, 60],0,10)


        queen = py.draw.rect(surface,'white',[250,300,150,50],0,10)
        rook = py.draw.rect(surface,'white', [250,375,150,50],0,10)
        bishop = py.draw.rect(surface,'white',[250,450,150,50],0,10)
        knight = py.draw.rect(surface,'white',[250,525,150,50],0,10)

        surface.blit(font.render('choose a piece',True,'black'),(WIDTH*2.1//8 + 10 ,HEIGHT*1.5//8 + 10))
        surface.blit(font.render('queen',True,'black'),(275,305))
        surface.blit(font.render('rook',True,'black'),(275,380))
        surface.blit(font.render('bishop',True,'black'),(275,455))
        surface.blit(font.render('knight',True,'black'),(275,530))

        while True:
            screen.blit(surface,(0,0))
            for event in py.event.get():
                if event.type==py.MOUSEBUTTONDOWN:
                    clicked_pos=event.pos
                    # print(clicked_pos)
                    if queen.collidepoint(event.pos):
                        
                        return 'q'
                    elif rook.collidepoint(event.pos):
    
                        return 'r'
                    elif knight.collidepoint(event.pos):
                        # print('knight')
                        return 'k'
                    elif bishop.collidepoint(event.pos):
                        # print('bishop')
                        return 'b'
                
                if event.type== py.QUIT:
                        py.quit()
                        sys.exit()


            py.display.update()




        

