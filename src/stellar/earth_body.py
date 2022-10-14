from core.fileUtils import FileUtils
from stellar.stellar_utils import StellarUtils
from stellar.body import Body
from material.earth_material import EarthMaterial
from core.texture import Texture

class Earth(Body):

    def __init__(self, position=[0, 0, 0]) -> None:
        unit_radius = StellarUtils.kmToUnits(6371)
        super().__init__(unit_radius, position=position)
        self._Material = EarthMaterial(
            texture=Texture(FileUtils.getAsset("earth.jpg")),
            bump_texture=Texture(FileUtils.getAsset("earth_bump.jpg")),
            use_shadows=True )