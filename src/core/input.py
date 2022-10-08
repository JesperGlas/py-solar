from typing import List
import pygame as pg

class Input(object):
    
    def __init__(self):
        self._Quit: bool = False
        self._KeyDownList: List = []
        self._KeyPressedList: List = []
        self._KeyUpList: List = []
        
    def update(self) -> None:
        # reset discrete key list
        self._KeyDownList = []
        self._KeyUpList = []
        
        for event in pg.event.get():
            # check if window registered quit event
            if event.type == pg.QUIT:
                self._Quit = True
            
            # check keyboard
            if event.type == pg.KEYDOWN:
                key_name = pg.key.name(event.key)
                self._KeyDownList.append(key_name)
                self._KeyPressedList.append(key_name)
            if event.type == pg.KEYUP:
                key_name = pg.key.name(event.key)
                self._KeyPressedList.remove(key_name)
                self._KeyUpList.append(key_name)

    def isKeyDown(self, key_code) -> bool:
        return key_code in self._KeyDownList

    def isKeyPressed(self, key_code) -> bool:
        return key_code in self._KeyPressedList

    def isKeyUp(self, key_code) -> bool:
        return key_code in self._KeyUpList