import pygame as pg

class Input(object):
    
    def __init__(self):
        self._Quit = False
        
    def update(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self._Quit = True