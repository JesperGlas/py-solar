from core.fileUtils import FileUtils
from stellar.stellar_utils import StellarUtils as SU
from core.texture import Texture
from material.texture_material import TextureMaterial
from geometry.sphere_geometry import SphereGeometry
from material.orbital_material import OrbitalMaterial
from core.mesh import Mesh

class Earth(Mesh):

    def __init__(self) -> None:

        earth_radius = SU.getEarthRadius()
        geo = SphereGeometry(radius=earth_radius, radius_segments=128, height_segments=64)
        mat = OrbitalMaterial(
            texture_name="earth.jpg",
            bumpmap_name="earth_bump.jpg",
            atmosphere_name="earth_clouds.jpg",
            use_shadows=True )
        super().__init__(geo, mat)
