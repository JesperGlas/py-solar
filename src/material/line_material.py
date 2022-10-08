from typing import Dict
from OpenGL.GL import *
from material.base_material import BaseMaterial

class LineMaterial(BaseMaterial):

    def __init__(self, properties: Dict = {}) -> None:
        super().__init__()

        self._Settings["drawStyle"] = GL_LINE_STRIP
        self._Settings["lineWidth"] = 1
        # line type: "connected" | "loop" | "segments"
        self._Settings["lineType"] = "connected"

        self.setProperties(properties)

    def updateRenderSettings(self) -> None:

        glLineWidth(self._Settings["lineWidth"])
        if self._Settings["lineType"] == "connected":
            self._Settings["drawStyle"] = GL_LINE_STRIP
        elif self._Settings["lineType"] == "loop":
            self._Settings["drawStyle"] = GL_LINE_LOOP
        elif self._Settings["lineType"] == "segments":
            self._Settings["drawStyle"] = GL_LINES
        else:
            raise Exception(f"Unknown LineMaterial draw style. [ connected | loop | segments ]")
        
        return super().updateRenderSettings()