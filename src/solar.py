from math import pi
from pathlib import Path
from typing import Dict

# core
from core.utils import OpenGLUtils
from core.base import Base
from core.renderer import Renderer
from core.render_target import RenderTarget
from core.object3D import Object3D

# scene
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh

# geometry
from geometry.sphere_geometry import SphereGeometry

# material
from material.material import Material
from material.surface_material import SurfaceMaterial
from material.lambert_material import LambertMaterial
from material.phong_material import PhongMaterial

# texture
from core.texture import Texture

# extra
from extras.movement_rig import MovementRig

# light
from light.ambient_light import AmbientLight
from light.directional_light import DirectionalLight

# postprocessing
from extras.post_processor import PostProcessor
from effects.bright_filter_effect import BrightFilterEffect
from effects.horizontal_blur_effect import HorizontalBlurEffect
from effects.vertical_blur_effect import VerticalBlurEffect
from effects.aditive_blend_effect import AdditiveBlendEffect

TITLE: str = "Solarpy"
VERSION: str = "1.0.0"
AUTHOR: str = "Jesper Glas"

class App(Base):

    def __init__(self, screen_size=[1280, 720], caption="App Window"):
        super().__init__(screen_size, caption)

        # print system information
        print(f"\nSystem information:")
        OpenGLUtils.printSystemInfo()

        # set up assets path
        self._Assets = f"{Path(__file__).resolve().parent}/assets/"
        print(f"Assets path set to: {self._Assets}")

    def initialize(self) -> None:
        self._Scene = Scene()
        self._Camera = Camera(aspect_ratio=1280/720)
        self._Renderer = Renderer(self._Scene, self._Camera, clear_color=True)
        
        # setup moving camera position
        self._CameraRig = MovementRig()
        self._CameraRig.add(self._Camera)
        self._CameraRig.setPosition([0, 0, 6])
        self._Scene.add(self._CameraRig)

        # set up light
        sun_light = DirectionalLight(
            color=[0.8, 0.8, 0.8],
            direction=[1, 1, -2] )
        self._Scene.add(sun_light)

        sun_ambient = AmbientLight(color=[1, 1, 1])

        # set up geometry
        sun_geo = SphereGeometry(2)
        earth_geo = SphereGeometry()

        # set up textures
        sun_tex = Texture(f"{self._Assets}/sun.jpg")
        earth_tex = Texture(f"{self._Assets}/earth.jpg")
        
        # bump maps
        earth_bump = Texture(f"{self._Assets}/earth_bump.jpg")

        # set up material
        sun_mat = LambertMaterial( texture=sun_tex )
        earth_mat = PhongMaterial( texture=earth_tex, bump_texture=earth_bump )

        # set up meshes
        self._Sun = Mesh(sun_geo, sun_mat)
        self._Sun.setPosition([-2, 0, 0])
        self._Scene.add(self._Sun)
        self._Sun.add(sun_ambient)
        
        self._Earth = Mesh(earth_geo, earth_mat)
        self._Earth.setPosition([2, 0, 0])
        self._Scene.add(self._Earth)

        # post processing
        self._PostProcessor = PostProcessor(self._Renderer, self._Scene, self._Camera)
        
        # scene info
        print(f"Scene info:")
        self._Scene.printNodeTree()
        
    def update(self) -> None:
        # update data
        self._CameraRig.update(self._Input, self._DeltaTime)
        self._Sun.rotateX(0.002)
        self._Earth.rotateX(0.002)
        
        # update uniforms

        # render
        self._PostProcessor.render()
    
App().run()