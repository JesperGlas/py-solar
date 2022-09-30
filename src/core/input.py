import pygame as pg

class Input(object):
    
    def __init__(self):
        self.quit = False
        
    def update(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit = True