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
from light.directional_light import DirectionalLight

# extra
from extras.movement_rig import MovementRig


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

        sun_geo = SphereGeometry(radius=10, radius_segments=128, height_segments=64)
        sun_mat = SunMaterial()
        self._Sun = Mesh(sun_geo, sun_mat)
        self._MainScene.add(self._Sun)

        earth_geo = SphereGeometry(radius_segments=64, height_segments=32)
        earth_mat = OrbitalMaterial(
            texture_name="earth.jpg",
            bumpmap_name="earth_bump.jpg",
            use_shadows=True
        )
        self._Earth = Mesh(earth_geo, earth_mat)
        self._Sun.add(self._Earth)
        self._Earth.setPosition([20, 0, 0])

        moon_geo = SphereGeometry(radius=0.5)
        moon_mat = OrbitalMaterial(
            texture_name="moon.jpg",
            bumpmap_name="moon_bump.jpg",
            use_shadows=True
        )
        self._Moon = Mesh(moon_geo, moon_mat)
        self._Earth.add(self._Moon)
        self._Moon.setPosition([0, 0, -4])

        # setup moving camera position
        self._CameraRig = MovementRig(units_per_sec=10)
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
            self._CameraRig.attach(self._Sun, distance=20)
            self._MainScene.printNodeTree()
        if self._Input.isKeyDown("2"):
            self._CameraRig.attach(self._Earth)
            self._MainScene.printNodeTree()
        if self._Input.isKeyDown("3"):
            self._CameraRig.attach(self._Moon, distance=2)
            self._MainScene.printNodeTree()
        
        # update sun
        self._Sun.rotateY(0.001)

        # update earth
        earth_rotation_speed = 0.001
        self._Earth.rotateY(earth_rotation_speed)
        self._CameraRig.rotateY(-earth_rotation_speed, False) # compensate for earth rotation
        self._Earth.rotateY(0.001, False)
        self._Earth._Material.setProperties(properties={
            "u_lightDirection": self._Earth.getWorldPosition(),
            "u_sunPosition": [0, 0, 0],
            "u_sunRadius": 2,
            "u_moonPosition": self._Moon.getWorldPosition(),
            "u_moonRadius": 0.5
        })

        # update moon
        moon_rotation_speed = 0.001
        self._Moon.rotateY(moon_rotation_speed)
        self._Moon.rotateY(0.001, False)
        self._Moon._Material.setProperties(properties={
            "u_lightDirection": self._Moon.getWorldPosition(),
            "u_sunPosition": [0, 0, 0],
            "u_sunRadius": 2,
            "u_moonPosition": self._Earth.getWorldPosition(),
            "u_moonRadius": 0.5
        })

        # update uniforms
        self._Sun._Material.setProperties(properties={
            "u_time": self._ElapsedTime })

        # render
        self._Renderer.render(self._MainScene, self._Camera)
    
App().run()