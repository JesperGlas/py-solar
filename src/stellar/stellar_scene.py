# python imports
from typing import List

# core imports
from core.fileUtils import FileUtils as FU
from core.scene import Scene
from core.camera import Camera
from core.texture import Texture
from core.mesh import Mesh
from core.input import Input

# extras

# stellar imports
from stellar.stellar_camera import StellarCamera
from stellar.stellar_body import StellarBody

class StellarScene(Scene):

    def __init__(self) -> None:
        super().__init__()

        self._Active = False

        # objects in scene
        self._Target: StellarBody = None
        self._Moons: List[StellarBody] = []

        # camera rig
        self._CameraRig = StellarCamera()
        self.add(self._CameraRig)
        self._CameraRig.resetCamera()

        # get camera from camera rig
        self._Camera = self._CameraRig._Camera

        self.initialize()

    def initialize(self) -> None:
        # target should be initialized in inherited initialize function
        if self._Target:
            self.add(self._Target)

    def update(self, input: Input, delta_time: float, elapsed_time: float) -> None:
        self._CameraRig.update(input, delta_time)

    def play(self) -> None:
        self._Active = True

    def stop(self) -> None:
        self._Active = False