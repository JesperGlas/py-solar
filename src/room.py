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
from geometry.box_geometry import BoxGeometry

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

        # setup room
        wall_geo = RectangleGeometry(20, 20)
        wall_mat = PhongMaterial(shininess=1, use_shadows=True, properties={
            "u_color": [0.8, 0.8, 0.8]
        })

        self._Floor = Mesh(wall_geo, wall_mat)
        self._Floor.setPosition([0, -10, 0])
        self._Floor.rotateX(-pi/2)
        self._Scene.add(self._Floor)

        self._rWall = Mesh(wall_geo, wall_mat)
        self._rWall.setPosition([-10, 0, 0])
        self._rWall.rotateY(pi/2)
        self._Scene.add(self._rWall)

        self._lWall = Mesh(wall_geo, wall_mat)
        self._lWall.setPosition([0, 0, -10])
        self._Scene.add(self._lWall)

        # set up objects
        sphere_geo = SphereGeometry()
        sphere_mat = PhongMaterial(use_shadows=True)
        self._Sphere1 = Mesh(sphere_geo, sphere_mat)
        self._Scene.add(self._Sphere1)
        self._Sphere2 = Mesh(sphere_geo, sphere_mat)
        self._Sphere2.setPosition([-3, -3, 0])
        self._Scene.add(self._Sphere2)
        
        # setup moving camera position
        self._CameraRig = MovementRig()
        self._CameraRig.add(self._Camera)
        self._CameraRig.setPosition([5, 5, 15])
        self._CameraRig.setDirection([-0.5, -0.5, -1])
        self._Scene.add(self._CameraRig)

        # set up light
        self._Ambient = AmbientLight(color=[0.2, 0.2, 0.2])
        self._Scene.add(self._Ambient)
        self._Directional = DirectionalLight()
        self._Directional.setDirection([-0.3, -0.3, 0])
        self._Scene.add(self._Directional)

        self._Renderer.enableShadows(self._Directional)

        # scene info
        print(f"Scene info:")
        self._Scene.printNodeTree()
        
    def update(self) -> None:
        # update
        self._CameraRig.update(self._Input, self._DeltaTime)
        if self._Input.isKeyPressed("space"):
            self._Directional.rotateY(-0.02, False)

        
        # render
        self._Renderer.render(self._Scene, self._Camera)    

App().run()