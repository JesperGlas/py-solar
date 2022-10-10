from math import pi
from pathlib import Path
from typing import Dict

# core
from core.utils import OpenGLUtils
from core.base import Base
from core.renderer import Renderer
from core.object3D import Object3D

# scene
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh

# geometry
from geometry.sphere_geometry import SphereGeometry

# material
from material.material import Material
from material.lambert_material import LambertMaterial

# texture
from core.texture import Texture
from material.texture_material import TextureMaterial

# extra
from extras.movement_rig import MovementRig

# light
from light.directional_light import DirectionalLight

# postprocessing
from extras.post_processor import PostProcessor
from effects.tint_effect import TintEffect

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
        self._Renderer = Renderer(self._Scene, self._Camera)
        
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

        # set up geometry
        sphere_geo = SphereGeometry()

        # set up textures
        earth_tex = Texture(f"{self._Assets}/sun.jpg")
        
        # bump maps
        earth_bump = Texture(f"{self._Assets}/earth_bump.jpg")

        # set up material
        lambert_mat = LambertMaterial( texture=earth_tex )

        # set up meshes
        self._Earth = Mesh(sphere_geo, lambert_mat)
        self._Earth.setPosition([0, 0, 0])
        self._Scene.add(self._Earth)

        # post processing
        self._PostProcessor = PostProcessor(self._Renderer, self._Scene, self._Camera)
        self._PostProcessor.addEffect(TintEffect(tint_color=[1, 0, 0]))

        # scene info
        print(f"Scene info:")
        self._Scene.printNodeTree()
        
    def update(self) -> None:
        # update data
        self._CameraRig.update(self._Input, self._DeltaTime)
        self._Earth.rotateX(0.002)
        
        # update uniforms

        # render
        self._PostProcessor.render()
    
App().run()