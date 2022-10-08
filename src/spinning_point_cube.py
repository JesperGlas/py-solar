from core.utils import OpenGLUtils
from core.base import Base
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from geometry.box_geometry import BoxGeometry
from material.point_material import PointMaterial

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
        self._Camera.setPosition([0, 0, 4])

        geometry = BoxGeometry()
        material = PointMaterial()
        self._Mesh = Mesh(geometry, material)
        self._Scene.add(self._Mesh)

    def update(self) -> None:
        self._Mesh.rotateY(0.0514)
        self._Mesh.rotateX(0.0337)
        self._Renderer.render(self._Scene, self._Camera)
    
App().run()