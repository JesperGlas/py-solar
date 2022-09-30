import pygame as pg
import sys
from core.input import Input

class Base(object):
    
    def __init__(self, screen_size=[512, 512]):
        
        pg.init()
        display_flags = pg.DOUBLEBUF | pg.OPENGL
        
        pg.display.gl_set_attribute(pg.GL_MULTISAMPLEBUFFERS, 1)
        pg.display.gl_set_attribute(pg.GL_MULTISAMPLESAMPLES, 4)
        pg.display.gl_set_attribute(
            pg.GL_CONTEXT_PROFILE_MASK,
            pg.GL_CONTEXT_PROFILE_CORE
        )
        self.screen = pg.display.set_mode(screen_size, display_flags)
        pg.display.set_caption("Solar System Simulation")
        
        self.running = True
        self.clock = pg.time.Clock()
        
        # for user input
        self.input = Input()
        
    def initilize(self) -> None:
        pass
    
    def update(self) -> None:
        self.input.update()
    
    def run(self) -> None:
        
        # startup
        self.initilize()
        
        # main loop
        while self.running:
            
            # handle input
            if self.input.quit:
                self.running = False
            
            # update
            self.update()
            
            # render
            pg.display.flip()
            
            # sync clock
            self.clock.tick(60)
            
        # shutdown
        pg.quit()
        sys.exit()