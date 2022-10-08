from typing import Dict
from material.base_material import BaseMaterial
from OpenGL.GL import *

class PointMaterial(BaseMaterial):

    def __init__(self, properties: Dict = {}) -> None:
        super().__init__()

        self._Settings["drawStyle"] = GL_POINTS
        self._Settings["pointSize"] = 8
        self._Settings["roundedPoints"] = False
        self.setProperties(properties)

    def updateRenderSettings(self) -> None:
        glPointSize(self._Settings["pointSize"])
        if self._Settings["roundedPoints"]:
            glEnable(GL_POINT_SMOOTH)
        else:
            glDisable(GL_POINT_SMOOTH)