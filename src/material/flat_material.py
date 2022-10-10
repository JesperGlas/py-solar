from typing import Dict, Tuple
from OpenGL.GL import *
from shaders.shaderUtils import ShaderUtils
from material.material import Material
from core.texture import Texture

class FlatMaterial(Material):

    def __init__(self, texture: Texture=None, properties: Dict={}) -> None:

        vert_code, frag_code = ShaderUtils.loadShaderCode("flat_material")
        print(vert_code)
        super().__init__(vert_code, frag_code)
        
        # add uniforms
        self.addUniform("vec3", "u_color", [1.0, 1.0, 1.0])
        self.addUniform("Light", "u_light0", None)
        self.addUniform("Light", "u_light1", None)
        self.addUniform("Light", "u_light2", None)
        self.addUniform("Light", "u_light3", None)
        self.addUniform("bool", "u_useTexture", 0)
        if texture == None:
            self.addUniform("bool", "u_useTexture", False)
        else:
            self.addUniform("bool", "u_useTexture", True)
            self.addUniform("sampler2D", "u_texture", [texture._TextureRef, 1])

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