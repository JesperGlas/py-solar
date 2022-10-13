from math import pi
from pathlib import Path
from typing import Dict

# core
from core.openGLUtils import OpenGLUtils
from core.fileUtils import FileUtils
from core.base import Base
from core.renderer import Renderer

# scene
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh

# geometry
from geometry.sphere_geometry import SphereGeometry
from geometry.rectangle_geometry import RectangleGeometry

# material
from material.lambert_material import LambertMaterial
from material.phong_material import PhongMaterial
from material.surface_material import SurfaceMaterial

# texture
from core.texture import Texture
from material.texture_material import TextureMaterial

# extra
from extras.movement_rig import MovementRig
from extras.post_processor import PostProcessor

# light
from light.ambient_light import AmbientLight
from light.directional_light import DirectionalLight

# stellar
from stellar.stellar_utils import StellarUtils
from stellar.sun import Sun

TITLE: str = "Solarpy"
VERSION: str = "1.0.0"
AUTHOR: str = "Jesper Glas"

class App(Base):

    def __init__(self, screen_size=[1280, 720], caption="App Window"):
        super().__init__(screen_size, caption)
        self._ScreenSize = screen_size

        # print system information
        print(f"\nSystem information:")
        OpenGLUtils.printSystemInfo()
        FileUtils.setProjectRoot()

    def initialize(self) -> None:
        self._Scene = Scene()
        self._Camera = Camera(aspect_ratio=self._ScreenSize[0]/self._ScreenSize[1])
        self._Renderer = Renderer(clear_color=[0, 0, 0])

        # set up stellar objects
        self._Sun = Sun()
        self._Scene.add(self._Sun)
        
        # setup moving camera position
        self._CameraRig = MovementRig(units_per_sec=StellarUtils.kmToUnits(1e6))
        self._CameraRig.add(self._Camera)
        self._CameraRig.setPosition([0, 0, StellarUtils.kmToUnits(1e6)])
        self._Scene.add(self._CameraRig)

        print(f"Camer: {self._Camera.getWorldPosition()}")
        print(f"Rig: {self._CameraRig.getWorldPosition()}")
        print(f"Sun: {self._Sun.getWorldPosition()}")

        # set up light
        self._Ambient = AmbientLight(color=[0.1, 0.1, 0.1])
        self._Scene.add(self._Ambient)
        self._SunLight = DirectionalLight(
            color=[0.8, 0.8, 0.8],
            direction=[0, 0, -1] )
        self._Scene.add(self._SunLight)

        # scene info
        print(f"Scene info:")
        self._Scene.printNodeTree()
        
    def update(self) -> None:
        # update
        self._CameraRig.update(self._Input, self._DeltaTime)
        if self._Input.isKeyPressed("space"):
            self._SunLight.rotateY(-0.02, False)

        
        # render
        self._Renderer.render(self._Scene, self._Camera)    

App().run()