from typing import List
from stellar.stellar_utils import StellarUtils as SU
from geometry.sphere_geometry import SphereGeometry
from material.orbital_material import OrbitalMaterial
from stellar.stellar_body import StellarBody
from light.occluder import Occluder

class Moon(StellarBody):

    def __init__(self, custom_radius=None) -> None:

        moon_radius = SU.getEarthRadius()
        if custom_radius != None:
            moon_radius = custom_radius
        geo = SphereGeometry(radius=moon_radius, radius_segments=128, height_segments=64)
        mat = OrbitalMaterial(
            color_tex_name="moon.jpg",
            bump_tex_name="moon_bump.jpg" )
        super().__init__(moon_radius, geo, mat)

        # create and add occluder for shadow calculation
        self._Occluder = Occluder(self.getWorldPosition(), moon_radius)
        self.add(self._Occluder)

    def setPosition(self, position: List=[0, 0, SU.getMoonEarthDistance()]):
        return super().setPosition(position)

    def update(self) -> None:
        rotation_speed = 0.001
        orbit_speed = 0.0001
        self.rotateY(rotation_speed)
        self.rotateY(orbit_speed, False)
