# core imports
from core.fileUtils import FileUtils
from core.mesh import Mesh
from core.input import Input

# geometry
from geometry.sphere_geometry import SphereGeometry

# material
from stellar.orbital_material import OrbitalMaterial
from stellar.atmosphere_material import AtmosphereMaterial

# stellar imports
from stellar.stellar_scene import StellarScene

# light
from light.light import Light

class EarthScene(StellarScene):

    def __init__(self) -> None:
        super().__init__()

    def initialize(self) -> None:

        # set up target
        geometry = SphereGeometry(radius_segments=128, height_segments=64)
        material = OrbitalMaterial(
            color_tex="earth.jpg",
            night_tex="earth_night.jpg",
            bump_tex="earth_bump.jpg",
            specular_tex="earth_specular.png",
            atmosphere_tex="earth_atmosphere.jpg" )
        self._Target = Mesh(geometry, material)

        # set up atmosphere
        geometry = SphereGeometry(1.02, radius_segments=128, height_segments=64)
        material = AtmosphereMaterial()
        atmosphere = Mesh(geometry, material)
        atmosphere.setPosition([0, 0, 0])
        #self._Target.add(atmosphere)

        # set up moons
        geometry = SphereGeometry(radius=0.27264, radius_segments=128, height_segments=64)
        material = OrbitalMaterial(
            color_tex="moon.jpg",
            bump_tex="moon_bump.jpg" )
        self._Moon = Mesh(geometry, material)
        self._Target.add(self._Moon)
        moon_distance = 1/6371 * 384400
        self._Moon.setPosition([moon_distance, 0, 0])

        # set up light
        self._Light = Light()
        self._Light.setPosition([-1e6, 0, 0])
        self._Target.add(self._Light)
        return super().initialize()

    def update(self, input: Input, delta_time: float, elapsed_time: float) -> None:
        self._Target.rotateY(0.001)
        self._Moon.rotateY(0.002)
        return super().update(input, delta_time, elapsed_time)