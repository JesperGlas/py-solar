# core imports
from core.fileUtils import FileUtils
from core.mesh import Mesh
from core.input import Input

# geometry
from geometry.sphere_geometry import SphereGeometry

# material
from material.orbital_material import OrbitalMaterial

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
            color_tex_name="earth.jpg",
            night_tex_name="earth_night.jpg",
            bump_tex_name="earth_bump.jpg",
            atmosphere_tex_name="earth_atmosphere.jpg" )
        self._Target = Mesh(geometry, material)

        # set up moons
        geometry = SphereGeometry(radius=0.27264, radius_segments=128, height_segments=64)
        material = OrbitalMaterial(
            color_tex_name="moon.jpg",
            bump_tex_name="moon_bump.jpg" )
        self._Moon = Mesh(geometry, material)
        self._Target.add(self._Moon)
        self._Moon.setPosition([3, 0, 0])

        # set up light
        self._Light = Light()
        self._Light.setPosition([-10, 0, 0])
        self._Target.add(self._Light)
        return super().initialize()

    def update(self, input: Input, delta_time: float, elapsed_time: float) -> None:
        self._Target.rotateY(0.001)
        self._Moon.rotateY(0.002)
        return super().update(input, delta_time, elapsed_time)