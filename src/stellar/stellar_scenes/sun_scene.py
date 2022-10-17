# core imports
from core.fileUtils import FileUtils
from core.mesh import Mesh
from core.input import Input

# geometry
from geometry.sphere_geometry import SphereGeometry

# material
from material.sun_material import SunMaterial
from stellar.atmosphere_material import AtmosphereMaterial

# stellar imports
from stellar.stellar_scene import StellarScene

class SunScene(StellarScene):

    def __init__(self) -> None:
        super().__init__()

    def initialize(self) -> None:
        geometry = SphereGeometry(radius_segments=128, height_segments=64)
        material = SunMaterial()
        self._Target = Mesh(geometry, material)
        self.add(self._Target)
        
        return super().initialize()

    def update(self, input: Input, delta_time: float, elapsed_time: float) -> None:
        self._Target._Material.setProperties({
            "u_time": elapsed_time
        })
        return super().update(input, delta_time, elapsed_time)
