from core.fileUtils import FileUtils
from stellar.stellar_utils import StellarUtils
from stellar.body import Body
from material.lambert_material import LambertMaterial
from core.texture import Texture

class Sun(Body):

    def __init__(self) -> None:
        unit_radius = StellarUtils.kmToUnits(6.9634e5)
        self._Material = LambertMaterial(
            texture=Texture(FileUtils.getAsset("sun.jpg")) )
        super().__init__(unit_radius, position=[0, 0, 0])