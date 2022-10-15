from shaders.shaderUtils import ShaderUtils
from typing import Dict
from OpenGL.GL import *
from shaders.shaderUtils import ShaderUtils
from material.material import Material
from core.texture import Texture

class TextureMaterial(Material):
    
    def __init__(self, texture: Texture, custom_shader_name: str=None, properties: Dict={}) -> None:

        if custom_shader_name:
            vert_code, frag_code = ShaderUtils.loadShaderCode(custom_shader_name)
        else:
            vert_code, frag_code = ShaderUtils.loadShaderCode("texture_shader")

        super().__init__(vert_code, frag_code)

        self.addUniform("vec3", "u_color", [1.0, 1.0, 1.0])
        self.addUniform("sampler2D", "u_texture", [texture._TextureRef, 1])
        self.addUniform("vec2", "u_texRepeat", [1.0, 1.0])
        self.addUniform("vec2", "u_texOffset", [0.0, 0.0])
        self.locateUniforms()

        # render both sides?
        self._Settings["doubleSided"] = True
        # render triangles as wireframe?
        self._Settings["onlyWireframe"] = False
        # line thickness for wireframe
        self._Settings["lineWidth"] = 1

        self.setProperties(properties)

    def updateRenderSettings(self) -> None:

        if self._Settings["doubleSided"]:
            glDisable( GL_CULL_FACE )
        else:
            glEnable( GL_CULL_FACE )
            
        if self._Settings["onlyWireframe"]:
            glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )
        else:
            glPolygonMode( GL_FRONT_AND_BACK, GL_FILL )

        glLineWidth( self._Settings["lineWidth"] )
        
        return super().updateRenderSettings()