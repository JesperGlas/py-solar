from typing import Dict
from material.base_material import BaseMaterial
from OpenGL.GL import *

class SurfaceMaterial(BaseMaterial):

    def __init__(self, properties: Dict={}) -> None:
        super().__init__()

        # render vertecies as surface
        self._Settings["drawStyle"] = GL_TRIANGLES
        # render both sides?
        # default: front side only
        #   vertecies ordered counterclockwise
        self._Settings["doubleSided"] = False
        # render triangles as wireframe?
        # default: No
        self._Settings["onlyWireframe"] = False
        # line thickness for wireframe
        self._Settings["lineWidth"] = 1

        self.setProperties(properties)

    def updateRenderSettings(self) -> None:

        if self._Settings["doubleSided"]:
            glDisable(GL_CULL_FACE)
        else:
            glEnable(GL_CULL_FACE)

        if self._Settings["onlyWireframe"]:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        glLineWidth(self._Settings["lineWidth"])
        
        return super().updateRenderSettings()