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
from geometry.rectangle_geometry import RectangleGeometry

# material
from material.lambert_material import LambertMaterial
from material.sun_material import SunMaterial

# texture
from core.texture import Texture
from material.texture_material import TextureMaterial

# extra
from extras.movement_rig import MovementRig
from extras.post_processor import PostProcessor

# effects
from effects.horizontal_blur_effect import HorizontalBlurEffect
from effects.vertical_blur_effect import VerticalBlurEffect
from effects.aditive_blend_effect import AdditiveBlendEffect

# light
from light.ambient_light import AmbientLight
from light.directional_light import DirectionalLight


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

        # setup moving camera position
        self._CameraRig = MovementRig()
        self._CameraRig.add(self._Camera)
        self._CameraRig.setDirection([0, 0, -1])
        self._CameraRig.setPosition([0, 0, 4])
        self._MainScene.add(self._CameraRig)

        sun_geo = SphereGeometry(radius_segments=64, height_segments=32)
        sun_mat = SunMaterial()
        self._Sun = Mesh(sun_geo, sun_mat)
        self._MainScene.add(self._Sun)

        # scene info
        print(f"Scene info:")
        self._MainScene.printNodeTree()
        
    def update(self) -> None:
        # update data
        self._CameraRig.update(self._Input, self._DeltaTime)
        self._Sun.rotateY(0.001)

        # update uniforms
        self._Sun._Material.setProperties(properties={
            "u_time": self._ElapsedTime })

        # render
        self._Renderer.render(self._MainScene, self._Camera)
    
App().run()