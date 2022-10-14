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
from material.earth_material import EarthMaterial

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
from stellar.stellar_utils import StellarUtils as su
from stellar.sun_body import Sun
from stellar.earth_body import Earth

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
        self._Scene = Scene()
        self._Camera = Camera(aspect_ratio=1280/720)
        self._Renderer = Renderer(clear_color=[0, 0, 0])

        # set up scene
        self._Sun = Sun()
        self._Scene.add(self._Sun)

        self._Earth = Earth()
        self._Earth.setPosition([su.kmToUnits(1.4925e8), 0, 0])
        self._SunEarthLight = DirectionalLight(
            color=[0.8, 0.8, 0.8],
            direction=[0, 0, -1] )
        self._Earth.add(self._SunEarthLight)
        self._Sun.add(self._Earth)

        # set up light
        self._Ambient = AmbientLight(color=[0.1, 0.1, 0.1])
        self._Scene.add(self._Ambient)

        # setup moving camera position
        self._CameraRig = MovementRig(units_per_sec=su.kmToUnits(1e6))
        self._CameraRig.add(self._Camera)
        self._CameraRig.setDirection([0, 0, -1])
        self._CameraRig.setPosition([0, 0, su.kmToUnits(1.2e6)])
        self._Earth.add(self._CameraRig)

        # shadows
        self._Renderer.enableShadows( shadow_light=self._SunEarthLight, strength=1, resolution=[1280, 720], bias=0.01 )

        # post processing

        # scene info
        print(f"Scene info:")
        self._Scene.printNodeTree()
        
    def update(self) -> None:
        # update data
        self._CameraRig.update(self._Input, self._DeltaTime)
        if self._Input.isKeyPressed("space"):
            self._SunEarthLight.rotateY(-0.02, False)

        self._Earth.rotateY(0.002, True)
        self._Earth.rotateX(0.2, False)
        
        # update uniforms

        # render
        self._Renderer.render(self._Scene, self._Camera)
    
App().run()