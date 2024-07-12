import pygame as py
from CONSTS import *
class Drag:
    def __init__(self) -> None:
        self.piece=None
        self.moved=False

        self.x_mouse=0
        self.y_mouse=0

        self.start_row=0
        self.start_col=0
    def update_mouse_pos(self,pos):
        self.x_mouse,self.y_mouse=pos

    def save_initital_piece(self,pos):
        self.start_row,self.start_col=pos

    def the_piece(self,piece):
        self.piece=piece
        self.moved=True

    def undrag_piece(self):
        self.piece=None
        self.moved=False
        
    def show_dragging_motion(self,screen):
        self.piece.set_img()
        image=py.image.load(self.piece.img)

        w=image.get_width()
        h=image.get_height()

        image2=py.transform.scale(image,(w*1.1, h*1.1))

        image_center_pos=(self.x_mouse,self.y_mouse)
        self.piece.img_rect= image2.get_rect(center=image_center_pos)

        screen.blit(image2,self.piece.img_rect)


        

