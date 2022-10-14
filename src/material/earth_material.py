from typing import Dict
from core.fileUtils import FileUtils
from core.texture import Texture
from material.planet_material import PlanetMaterial
from core.object3D import Object3D

class EarthMaterial(PlanetMaterial):

    def __init__(self, properties: Dict = {}) -> None:
        texture =   Texture( FileUtils.getAsset("earth.jpg") )
        bump =      Texture( FileUtils.getAsset("earth_bump.jpg") )
        super().__init__(texture, bump, None, properties)