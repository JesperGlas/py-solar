# python imports
from typing import List

# core
from core.openGLUtils import OpenGLUtils
from core.fileUtils import FileUtils
from core.base import Base
from core.renderer import Renderer

# scene
from stellar.stellar_scene import StellarScene
from stellar.stellar_scenes.sun_scene import SunScene

# geometry

# material

# extra

TITLE: str = "Solarpy"
VERSION: str = "1.0.0"
AUTHOR: str = "Jesper Glas"

class App(Base):

    def __init__(self, screen_size=[1280, 720], caption="App Window"):
        super().__init__(screen_size, caption)

        # print system information
        print(f"\nSystem information:")
        OpenGLUtils.printSystemInfo()
        FileUtils.setProjectRoot()

    def initialize(self) -> None:
        self._Renderer = Renderer(clear_color=[0, 0, 0])

        self._ActiveScene = SunScene()
        self._SceneList: List[StellarScene] = [self._ActiveScene]

        # scene info
        print(f"Scene info:")
        self._ActiveScene.printNodeTree()
        
    def update(self) -> None:
        # update data
        self._ActiveScene.update(self._Input, self._DeltaTime, self._ElapsedTime)

        # render
        self._Renderer.render(self._ActiveScene, self._ActiveScene._Camera)
    
App().run()