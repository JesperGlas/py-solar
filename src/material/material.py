from typing import Dict
from core.utils import OpenGLUtils
from core.uniform import Uniform
from OpenGL.GL import *

class Material(object):

    def __init__(self, vert_code: str, frag_code: str) -> None:
        self._ProgramRef = OpenGLUtils.initializeProgram(vert_code, frag_code)

        self._Uniforms: Dict[str, Uniform] = {}

        self._Uniforms["u_model"]   = Uniform("mat4", None)
        self._Uniforms["u_view"]    = Uniform("mat4", None)
        self._Uniforms["u_proj"]    = Uniform("mat4", None)

        self._Settings: Dict = {}
        self._Settings["drawStyle"] = GL_TRIANGLES

    def addUniform(self, data_type: str, variable_name: str, data) -> None:
        self._Uniforms[variable_name] = Uniform(data_type, data)

    def locateUniforms(self) -> None:
        uniform_object: Uniform
        for variable_name, uniform_object in self._Uniforms.items():
            uniform_object.locateVariable(variable_name, self._ProgramRef)

    def updateRenderSettings(self) -> None:
        pass

    def setProperties(self, properties: Dict[str, Uniform]) -> None:
        for name, data in properties.items():
            if name in self._Uniforms.keys():
                self._Uniforms[name]._Data = data
            elif name in self._Settings.keys():
                self._Settings[name] = data
            else:
                raise Exception(f"Material has no property named: {name}")