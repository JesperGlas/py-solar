from stellar.stellar_utils import StellarUtils as SU
from geometry.sphere_geometry import SphereGeometry
from material.orbital_material import OrbitalMaterial
from core.mesh import Mesh
from light.occluder import Occluder

class Moon(Mesh):

    def __init__(self, custom_radius=None) -> None:

        moon_radius = SU.getEarthRadius()
        if custom_radius != None:
            moon_radius = custom_radius
        geo = SphereGeometry(radius=moon_radius, radius_segments=128, height_segments=64)
        mat = OrbitalMaterial(
            texture_name="moon.jpg",
            bumpmap_name="moon_bump.jpg" )
        super().__init__(geo, mat)

        # create and add occluder for shadow calculation
        self._Occluder = Occluder(self.getWorldPosition(), moon_radius)
        self.add(self._Occluder)
