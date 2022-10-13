from typing import Dict
from OpenGL.GL import *
from shaders.shaderUtils import ShaderUtils
from material.material import Material
from core.texture import Texture

class PhongMaterial(Material):

    def __init__(self, 
        texture: Texture=None,
        bump_texture: Texture=None,
        specular: float=1,
        shininess: float=32,
        use_shadows: bool=False,
        properties: Dict={}) -> None:
        
        vert_code, frag_code = ShaderUtils.loadShaderCode("phong_material")
        super().__init__(vert_code, frag_code)
        
        # add base uniforms
        self.addUniform("vec3", "u_color", [1.0, 1.0, 1.0])

        # light uniforms
        self.addUniform("Light", "u_light0", None)
        self.addUniform("Light", "u_light1", None)
        self.addUniform("Light", "u_light2", None)
        self.addUniform("Light", "u_light3", None)
        self.addUniform("vec3", "u_viewPosition", [0, 0, 0])
        self.addUniform("float", "u_specularStrength", specular)
        self.addUniform("float", "u_shininess", shininess)

        # texture uniforms
        self.addUniform("bool", "u_useTexture", 0)
        if texture == None:
            self.addUniform("bool", "u_useTexture", False)
        else:
            self.addUniform("bool", "u_useTexture", True)
            self.addUniform("sampler2D", "u_texture", [texture._TextureRef, 1])

        # bump map uniforms
        if bump_texture == None:
            self.addUniform("bool", "u_useBumpTexture", False)
        else:
            self.addUniform("bool", "u_useBumpTexture", True)
            self.addUniform("sampler2D", "u_bumpTexture", [bump_texture._TextureRef, 2])
            self.addUniform("float", "u_bumpStrength", 1.0)

        # add shadow uniforms
        if not use_shadows:
            self.addUniform("bool", "u_useShadow", False)
        else:
            self.addUniform("bool", "u_useShadow", True)
            self.addUniform("Shadow", "u_shadow0", None)

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