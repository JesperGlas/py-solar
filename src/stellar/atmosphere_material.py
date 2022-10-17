from typing import Dict
from OpenGL.GL import *
from core.fileUtils import FileUtils
from shaders.shaderUtils import ShaderUtils
from material.material import Material
from core.texture import Texture

class AtmosphereMaterial(Material):

    def __init__(self, color=[0, 0, 0.2, 0.2], properties: Dict={}) -> None:

        vert_code, frag_code = ShaderUtils.loadShaderCode("atmosphere_shader")
        super().__init__(vert_code, frag_code)
        
        # add base uniforms
        self.addUniform("vec4", "u_color", color)

        # light uniforms
        self.addUniform("Light", "u_light", None)
        self.addUniform("vec3", "u_viewPosition", [0, 0, 0])
        self.addUniform("vec3", "u_objectPosition", [0, 0, 0])
        
        # add shadow uniforms

        # add texture uniforms

        self.locateUniforms()

        # render both sides?
        self._Settings["doubleSided"] = True
        # render triangles as wireframe?
        self._Settings["onlyWireFrame"] = False
        # line thickness for wireframe rendering
        self._Settings["lineWidth"] = 1

        self.setProperties( properties )

    def updateRenderSettings(self) -> None:

        if self._Settings["doubleSided"]:
            glDisable( GL_CULL_FACE )
        else:
            glEnable( GL_CULL_FACE )

        if self._Settings["onlyWireFrame"]:
            glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )
        else:
            glPolygonMode( GL_FRONT_AND_BACK, GL_FILL )
        
        glLineWidth(self._Settings["lineWidth"])