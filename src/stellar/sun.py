from math import pi
from stellar.stellar_utils import StellarUtils as SU
from geometry.sphere_geometry import SphereGeometry
from material.sun_material import SunMaterial
from stellar.stellar_body import StellarBody
from light.sun_light import SunLight

class Sun(StellarBody):

    def __init__(self, custom_radius=None) -> None:

        sun_radius = SU.getSunRadius()
        if custom_radius != None:
            sun_radius = custom_radius
        geo = SphereGeometry(radius=sun_radius, radius_segments=128, height_segments=64)
        mat = SunMaterial()
        super().__init__(sun_radius, geo, mat)

        # add light component to sun
        self._Light = SunLight()
        self._Light._Radius = sun_radius
        self._Light.setPosition(self.getWorldPosition())
        self.add(self._Light)

    def update(self, speed: float = 1) -> None:
        angle = 0.001
        self.rotateY(angle)