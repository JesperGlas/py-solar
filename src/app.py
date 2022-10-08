from math import pi

# core
from core.utils import OpenGLUtils
from core.base import Base
from core.renderer import Renderer

# scene
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from material.material import Material
from geometry.sphere_geometry import SphereGeometry

# extra
from extras.visual_axes import VisualAxes
from extras.visual_grid import VisualGrid

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
        
        # set camera position
        self._Camera.setPosition([0.5, 1, 5])

        # extras

        axes = VisualAxes(axis_length=2)
        self._Scene.add(axes)

        grid = VisualGrid(
            size=20,
            grid_color=[1, 1, 1],
            center_color=[1, 1, 0],
        )
        grid.rotateX(-pi/2)
        self._Scene.add(grid)

    def update(self) -> None:
        # update uniforms

        # render
        self._Renderer.render(self._Scene, self._Camera)
    
App().run()