# python imports
from typing import List

# core
from core.openGLUtils import OpenGLUtils
from core.fileUtils import FileUtils
from core.base import Base
from core.renderer import Renderer

# scene
from stellar.stellar_scene import StellarScene

# predefined scenes
from stellar.stellar_scenes.sun_scene import SunScene
from stellar.stellar_scenes.earth_scene import EarthScene

# geometry

# material

# extra

TITLE: str = "Solarpy"
VERSION: str = "1.0.0"
AUTHOR: str = "Jesper Glas"

class App(Base):

    def __init__(self, screen_size=[1920, 1080], caption="App Window"):
        super().__init__(screen_size, caption)

        # print system information
        print(f"\nSystem information:")
        OpenGLUtils.printSystemInfo()
        FileUtils.setProjectRoot()

    def initialize(self) -> None:
        self._Renderer = Renderer(clear_color=[0, 0, 0])

        # init scene list for additional scenes
        self._SceneList: List[StellarScene] = []

        # add aditional scenes
        self._SceneList.append(SunScene())
        self._SceneList.append(EarthScene())

        # set an active scene
        self._ActiveScene = self._SceneList[1]
        self._ActiveScene.play()

        # scene info
        print(f"Scene info:")
        self._ActiveScene.printNodeTree()
        
    def update(self) -> None:
        # input
        if self._Input.isKeyPressed("escape"):
            self._Running = False
        if self._Input.isKeyUp("1"):
            # stop current active scene
            self._ActiveScene.stop()
            # set new active scene
            self._ActiveScene = self._SceneList[0]
            # play new active scene
            self._ActiveScene.play()
        if self._Input.isKeyUp("2"):
            self._ActiveScene.stop()
            self._ActiveScene = self._SceneList[1]
            self._ActiveScene.play()
        
        # update data
        self._ActiveScene.update(self._Input, self._DeltaTime, self._ElapsedTime)

        # render
        self._Renderer.render(self._ActiveScene, self._ActiveScene._Camera)
    
App().run()