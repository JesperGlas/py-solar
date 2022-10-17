# core imports
from core.fileUtils import FileUtils as FU
from core.scene import Scene
from core.camera import Camera
from core.texture import Texture
from core.mesh import Mesh
from core.input import Input

# geometry imports
from geometry.sphere_geometry import SphereGeometry

# material imports
from material.texture_material import TextureMaterial

# extras

# stellar imports
from stellar.stellar_camera import StellarCamera

class StellarScene(Scene):

    def __init__(self) -> None:
        super().__init__()

        self._Active = True

        # objects in scene
        self._Target = None
        self._Moons = []

        # camera rig
        self._CameraRig = StellarCamera()
        self.add(self._CameraRig)
        self._CameraRig.resetCamera()

        # get camera from camera rig
        self._Camera = self._CameraRig._Camera

        self.initialize()

    def initialize(self) -> None:
        pass

    def update(self, input: Input, delta_time: float, elapsed_time: float) -> None:
        self._CameraRig.update(input, delta_time)

    def play(self) -> None:
        self._Active = True

    def stop(self) -> None:
        self._Active = False