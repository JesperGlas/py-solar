from core.mesh import Mesh
from geometry.sphere_geometry import SphereGeometry
from material.lambert_material import LambertMaterial

class Body(Mesh):

    def __init__(self, radius=1, position=[0, 0, 0]) -> None:
        super().__init__(SphereGeometry(radius_segments=64, height_segments=32), LambertMaterial())