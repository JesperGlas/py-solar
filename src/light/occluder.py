from typing import List
from core.object3D import Object3D

class Occluder(Object3D):

    def __init__(self, position: List[float]=[0, 0, 0], radius: float=1) -> None:
        super().__init__()
        self._Position = position
        self._Radius = radius