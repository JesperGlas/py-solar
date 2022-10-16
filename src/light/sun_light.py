from light.light import Light
from core.mesh import Mesh
from geometry.geometry import Geometry
from geometry.sphere_geometry import SphereGeometry

class SunLight(Light):

    def __init__(self) -> None:
        super().__init__()

        # sunlight is supposed to be attached to a spehere (The sun)
        #   when that is the case, set light radius to the same as
        #   the radius attribute of the sphere geometry
        if self._Parent and isinstance(self._Parent, Mesh):
            self._Parent: Mesh
            self._Radius = self._Parent._Geometry._Attributes["a_radius"]._Data