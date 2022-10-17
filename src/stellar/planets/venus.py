from typing import List
from stellar.stellar_utils import StellarUtils as SU
from geometry.sphere_geometry import SphereGeometry
from material.orbital_material import OrbitalMaterial
from stellar.stellar_body import StellarBody
from light.occluder import Occluder

class Venus(StellarBody):

    def __init__(self, custom_radius=None) -> None:

        venus_radius = SU.getVenusRadius()
        if custom_radius != None:
            venus_radius = custom_radius
        geo = SphereGeometry(radius=venus_radius, radius_segments=128, height_segments=64)
        mat = OrbitalMaterial(
            color_tex_name="venus.jpg",
            atmosphere_tex_name="venus_atmosphere.jpg" )
        super().__init__(venus_radius, geo, mat)

        # create and add occluder for shadow calculation

    def setPosition(self, position: List=[0, 0, SU.getVenusSunDistance()]):
        return super().setPosition(position)

    def update(self) -> None:
        rotation_speed = 0.001
        orbit_speed = 0.0001
        self.rotateY(rotation_speed)
        self.rotateY(orbit_speed, False)