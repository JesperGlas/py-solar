from math import pi
from pathlib import Path

# core
from core.utils import OpenGLUtils
from core.base import Base
from core.renderer import Renderer

# scene
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from material.surface_material import SurfaceMaterial
from geometry.rectangle_geometry import RectangleGeometry

# texture
from core.texture import Texture
from material.texture_material import TextureMaterial

# extra
from extras.movement_rig import MovementRig

TITLE: str = "Solarpy"
VERSION: str = "1.0.0"
AUTHOR: str = "Jesper Glas"

class App(Base):

    def __init__(self, screen_size=[1280, 720], caption="Main Window"):
        super().__init__(screen_size, caption)

        # print system information
        print(f"\nSystem information:")
        OpenGLUtils.printSystemInfo()

    def initialize(self) -> None:
        self._Renderer = Renderer()
        self._Scene = Scene()
        self._Camera = Camera(aspect_ratio=1280/720)
        
        # setup moving camera position
        self._Rig = MovementRig()
        self._Rig.add(self._Camera)
        self._Rig.setPosition([0.5, 1, 5])
        self._Scene.add(self._Rig)

        geo = RectangleGeometry()
        source_path = Path(__file__).resolve().parent
        print(f"Loading assets from: {source_path}/assets")
        crate = Texture(f"{source_path}/assets/crate.jpg")
        mat = TextureMaterial(crate)
        mesh = Mesh(geo, mat)
        self._Scene.add(mesh)

    def update(self) -> None:
        # update data
        self._Rig.update(self._Input, self._DeltaTime)
        
        # update uniforms

        # render
        self._Renderer.render(self._Scene, self._Camera)
    
App().run()