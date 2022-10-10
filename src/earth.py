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
from extras.post_processor import PostProcessor

# light
from light.ambient_light import AmbientLight
from light.directional_light import DirectionalLight

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
        self._Ambient = AmbientLight(color=[0.1, 0.1, 0.1])
        self._Scene.add(self._Ambient)
        self._SunLight = DirectionalLight(
            color=[0.8, 0.8, 0.8],
            direction=[1, 0, -1] )
        self._Scene.add(self._SunLight)

        # set up geometry
        earth_geo = SphereGeometry(2)
        moon_geo = SphereGeometry(0.5)

        # set up textures
        earth_tex = Texture(f"{self._Assets}/earth.jpg")
        moon_tex = Texture(f"{self._Assets}/moon.jpg")
        
        # bump maps
        earth_bump = Texture(f"{self._Assets}/earth_bump.jpg")
        moon_bump = Texture(f"{self._Assets}/moon_bump.jpg")

        # set up material
        earth_mat = LambertMaterial( texture=earth_tex, bump_texture=earth_bump, use_shadows=True )
        moon_mat = LambertMaterial( texture=moon_tex, bump_texture=moon_bump, use_shadows=True )

        # set up meshes
        self._Earth = Mesh(earth_geo, earth_mat)
        self._Earth.setPosition([0, 0, 0])
        self._Scene.add(self._Earth)

        self._Moon = Mesh(moon_geo, moon_mat)
        self._Moon.setPosition([-2, 0, 2])
        self._Scene.add(self._Moon)

        # shadows
        self._Renderer.enableShadows( shadow_light=self._SunLight )

        # post processing

        # scene info
        print(f"Scene info:")
        self._Scene.printNodeTree()
        
    def update(self) -> None:
        # update data
        self._CameraRig.update(self._Input, self._DeltaTime)
        self._SunLight.rotateX(0.01337)
        
        # update uniforms

        # render
        self._Renderer.render(self._Scene, self._Camera)
    
App().run()