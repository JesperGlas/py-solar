from core.mesh import Mesh
from geometry.geometry import Geometry
from material.material import Material

class StellarBody(Mesh):

    def __init__(self, radius: float, geometry: Geometry, material: Material) -> None:
        self._Radius = radius
        super().__init__(geometry, material)

    def getRadius(self) -> float:
        return self._Radius

    def update(self, speed: float=1) -> None:
        # implemented by subclasses
        pass