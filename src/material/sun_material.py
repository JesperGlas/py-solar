from shaders.shaderUtils import ShaderUtils
from core.fileUtils import FileUtils
from typing import Dict
from OpenGL.GL import *
from material.material import Material
from core.texture import Texture

class SunMaterial(Material):
    
    def __init__(self, properties: Dict={}) -> None:

        vert_code, frag_code = ShaderUtils.loadShaderCode("sun_material")

        super().__init__(vert_code, frag_code)

        texture = Texture(FileUtils.getAsset("sun.jpg"))

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