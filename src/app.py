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
from geometry.box_geometry import BoxGeometry

# material
from material.material import Material
from material.surface_material import SurfaceMaterial
from material.flat_material import FlatMaterial
from material.lambert_material import LambertMaterial
from material.phong_material import PhongMaterial

# texture
from core.texture import Texture
from material.texture_material import TextureMaterial

# extra
from extras.movement_rig import MovementRig

# light
from light.ambient_light import AmbientLight
from light.directional_light import DirectionalLight
from light.point_light import PointLight

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
        self._Renderer = Renderer()
        self._Scene = Scene()
        self._Camera = Camera(aspect_ratio=1280/720)
        
        # setup moving camera position
        self._CameraRig = MovementRig()
        self._CameraRig.add(self._Camera)
        self._CameraRig.setPosition([0, 0, 6])
        self._Scene.add(self._CameraRig)

        # set up light
        ambient = AmbientLight( color=[0.1, 0.1, 0.1] )
        self._Scene.add(ambient)
        directional = DirectionalLight(
            color=[0.8, 0.8, 0.8],
            direction=[-1, -1, -2] )
        self._Scene.add(directional)
        point = PointLight(
            color=[0.9, 0, 0],
            position=[1, 1, 0.8] )
        self._Scene.add(point)

        # set up geometry
        sphere_geo = SphereGeometry()
        box_geo = BoxGeometry(width=1.5, height=1.5, depth=1.5)

        # set up textures
        earth_tex = Texture(f"{self._Assets}/earth.jpg")
        crate_tex = Texture(f"{self._Assets}/crate.jpg")

        # set up material
        flat_mat = FlatMaterial(properties={
            "u_color": [0.6, 0.2, 0.2]
        })
        lambert_mat = LambertMaterial( texture=earth_tex )
        phong_mat = PhongMaterial(texture=earth_tex, properties={
            "u_color": [0.5, 0.5, 1.0]
        })

        # set up meshes
        sphere1 = Mesh(sphere_geo, flat_mat)
        sphere1.setPosition([-2.5, 0, 0])
        self._Scene.add(sphere1)
        sphere2 = Mesh(sphere_geo, lambert_mat)
        sphere2.setPosition([0, 0, 0])
        self._Scene.add(sphere2)
        sphere3 = Mesh(sphere_geo, phong_mat)
        sphere3.setPosition([2.5, 0, 0])
        self._Scene.add(sphere3)

        # scene info
        print(f"Scene info:")
        self._Scene.printNodeTree()
        
    def update(self) -> None:
        # update data
        self._CameraRig.update(self._Input, self._DeltaTime)
        
        # update uniforms

        # render
        self._Renderer.render(self._Scene, self._Camera)
    
App().run()