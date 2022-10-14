from core.fileUtils import FileUtils
from stellar.stellar_utils import StellarUtils
from stellar.body import Body
from material.texture_material import TextureMaterial
from core.texture import Texture

class Sun(Body):

    def __init__(self, position=[0, 0, 0]) -> None:
        unit_radius = StellarUtils.kmToUnits(696034)
        super().__init__(unit_radius, position=position)
        self._Material = TextureMaterial(
            texture=Texture(FileUtils.getAsset("sun.jpg")) )