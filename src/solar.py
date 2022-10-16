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

# material
from material.orbital_material import OrbitalMaterial

# extra
from extras.movement_rig import MovementRig
from stellar.stellar_utils import StellarUtils as SU
from stellar.stellar_body import StellarBody
from stellar.planets.earth import Earth
from stellar.sun import Sun
from stellar.moons.moon import Moon

TITLE: str = "Solarpy"
VERSION: str = "1.0.0"
AUTHOR: str = "Jesper Glas"

class App(Base):

    def __init__(self, screen_size=[1280, 720], caption="App Window"):
        super().__init__(screen_size, caption)

        self._Resolution = screen_size

        # print system information
        print(f"\nSystem information:")
        OpenGLUtils.printSystemInfo()
        FileUtils.setProjectRoot()

    def initialize(self) -> None:
        self._MainScene = Scene()
        self._Camera = Camera(aspect_ratio=1280/720)
        self._Renderer = Renderer(clear_color=[0, 0, 0])

        self._Sun = Sun()
        self._MainScene.add(self._Sun)
        self._Sun.setPosition([0, 0, 0])

        self._Earth = Earth()
        self._Sun.add(self._Earth)
        self._Earth.setPosition()

        self._Moon = Moon()
        self._Earth.add(self._Moon)
        self._Moon.setPosition()

        # setup moving camera position
        self._CameraRig = MovementRig(units_per_sec=1)
        self._CameraRig.add(self._Camera)
        self._CameraRig.setDirection([0, 0, -1])
        self._CameraRig.setPosition([0, 0, 10])
        self._Earth.add(self._CameraRig)

        # scene info
        print(f"Scene info:")
        self._MainScene.printNodeTree()
        
    def update(self) -> None:
        # update data
        self._CameraRig.update(self._Input, self._DeltaTime)
        if self._Input.isKeyDown("1"):
            self._CameraRig.attach(self._Sun, self._Sun.getRadius()*3)
            self._MainScene.printNodeTree()
        if self._Input.isKeyDown("2"):
            self._CameraRig.attach(self._Earth, self._Earth.getRadius()*3)
            self._MainScene.printNodeTree()
        if self._Input.isKeyDown("3"):
            self._CameraRig.attach(self._Moon, self._Moon.getRadius()*3)
            self._MainScene.printNodeTree()

        # update stellar objects
        stellar_list = list( filter(
            lambda x: isinstance(x, StellarBody),
            self._MainScene.getDescendantList()) )
        stellar_body: StellarBody
        for stellar_body in stellar_list:
            stellar_body.update()

        # update uniforms
        self._Sun._Material.setProperties(properties={
            "u_time": self._ElapsedTime })

        self._Earth._Material.setProperties(properties={
            "u_time": self._ElapsedTime })

        # render
        self._Renderer.render(self._MainScene, self._Camera)
    
App().run()