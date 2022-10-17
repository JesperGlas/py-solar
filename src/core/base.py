import pygame as pg
import sys
from core.input import Input

class Base(object):
    
    def __init__(self, screen_size=[512, 512], caption="Main Window", fps=60):
        
        pg.init()

        display_flags = pg.DOUBLEBUF | pg.OPENGL
        pg.display.gl_set_attribute(pg.GL_MULTISAMPLEBUFFERS, 1)
        pg.display.gl_set_attribute(pg.GL_MULTISAMPLESAMPLES, 4)
        pg.display.gl_set_attribute(
            pg.GL_CONTEXT_PROFILE_MASK,
            pg.GL_CONTEXT_PROFILE_CORE )
        self._Screen = pg.display.set_mode(screen_size, display_flags)
        pg.display.set_caption(caption)

        # save screen resolution for child classes
        self._Resolution = screen_size
        
        self._Running = True
        self._Clock = pg.time.Clock()
        
        # for user input
        self._Input = Input()

        # runtime
        self._ElapsedTime = 0
        
    def initialize(self) -> None:
        print("Initializing..")
        # specify in inherited class
        pass
    
    def update(self) -> None:
        # specify in inherited class
        pass

    def shutdown(self) -> None:
        print("Shutting down..")
        pg.quit()
        sys.exit()
    
    def run(self) -> None:
        print("Running..")
        
        # startup
        self.initialize()
        
        # main loop
        while self._Running:
            
            # handle input
            self._Input.update()
            if self._Input._Quit:
                self._Running = False
            
            # update time
            self._DeltaTime = self._Clock.get_time() / 1000
            self._ElapsedTime += self._DeltaTime

            # update
            self.update()
            
            # render
            pg.display.flip()
            
            # sync clock
            self._Clock.tick(60)
            
        # shutdown
        self.shutdown()