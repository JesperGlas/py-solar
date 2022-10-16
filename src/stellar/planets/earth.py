from stellar.stellar_utils import StellarUtils as SU
from geometry.sphere_geometry import SphereGeometry
from material.orbital_material import OrbitalMaterial
from core.mesh import Mesh
from light.occluder import Occluder

class Earth(Mesh):

    def __init__(self, custom_radius=None) -> None:

        earth_radius = SU.getEarthRadius()
        if custom_radius != None:
            earth_radius = custom_radius
        geo = SphereGeometry(radius=earth_radius, radius_segments=128, height_segments=64)
        mat = OrbitalMaterial(
            texture_name="earth.jpg",
            bumpmap_name="earth_bump.jpg",
            atmosphere_name="earth_clouds.jpg")
        super().__init__(geo, mat)

        # create and add occluder for shadow calculation
        self._Occluder = Occluder(self.getWorldPosition(), earth_radius)
        self.add(self._Occluder)