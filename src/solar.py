from math import pi
from pathlib import Path
from typing import Dict

# core
from core.openGLUtils import OpenGLUtils
from core.fileUtils import FileUtils
from core.base import Base
from core.renderer import Renderer
from core.render_target import RenderTarget

# scene
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh

# geometry
from geometry.sphere_geometry import SphereGeometry

# material
from material.sun_material import SunMaterial
from material.orbital_material import OrbitalMaterial

# light
from light.light import Light

# extra
from extras.movement_rig import MovementRig
from stellar.stellar_utils import StellarUtils as SU
from stellar.planets.earth import Earth


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

        print(f"Sun radius: {SU.getSunRadius()}")
        print(f"Moon radius: {SU.getMoonRadius()}")

        sun_geo = SphereGeometry(radius=SU.getSunRadius(), radius_segments=128, height_segments=64)
        sun_mat = SunMaterial()
        self._Sun = Mesh(sun_geo, sun_mat)
        self._MainScene.add(self._Sun)

        self._Earth = Earth()
        self._Sun.add(self._Earth)
        self._Earth.setPosition([0, 0, SU.getEarthSunDistance()])

        moon_geo = SphereGeometry(radius=SU.getMoonRadius(), radius_segments=64, height_segments=32)
        moon_mat = OrbitalMaterial(
            texture_name="moon.jpg",
            use_shadows=True
        )
        self._Moon = Mesh(moon_geo, moon_mat)
        self._Earth.add(self._Moon)
        self._Moon.setPosition([SU.getMoonEarthDistance(), 0, 0])

        # setup moving camera position
        self._CameraRig = MovementRig(units_per_sec=0.5)
        self._CameraRig.add(self._Camera)
        self._CameraRig.setDirection([0, 0, -1])
        self._CameraRig.setPosition([0, 0, 10])
        self._Earth.add(self._CameraRig)

        # setup light
        self._Light = Light()
        self._Light.setPosition([0, 0, 0])
        self._MainScene.add(self._Light)

        # scene info
        print(f"Scene info:")
        self._MainScene.printNodeTree()
        
    def update(self) -> None:
        # update data
        self._CameraRig.update(self._Input, self._DeltaTime)
        if self._Input.isKeyDown("1"):
            self._CameraRig.attach(self._Sun, distance=SU.getSunRadius()*2)
            self._MainScene.printNodeTree()
        if self._Input.isKeyDown("2"):
            self._CameraRig.attach(self._Earth, distance=SU.getEarthRadius()*2)
            self._MainScene.printNodeTree()
        if self._Input.isKeyDown("3"):
            self._CameraRig.attach(self._Moon, distance=SU.getMoonRadius()*2)
            self._MainScene.printNodeTree()
        
        # update sun
        self._Sun.rotateY(0.001)

        # update earth
        earth_rotation_speed = 0.0001
        self._Earth.rotateY(earth_rotation_speed)

        # update moon
        moon_rotation_speed = 0.0001
        self._Moon.rotateY(moon_rotation_speed)

        # update uniforms
        self._Sun._Material.setProperties(properties={
            "u_time": self._ElapsedTime })

        # render
        self._Renderer.render(self._MainScene, self._Camera)
    
App().run()