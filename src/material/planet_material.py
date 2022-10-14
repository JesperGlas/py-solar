from typing import Dict
from OpenGL.GL import *
from shaders.shaderUtils import ShaderUtils
from material.material import Material
from core.texture import Texture
from light.ambient_light import AmbientLight
from light.directional_light import DirectionalLight
from core.object3D import Object3D

class PlanetMaterial(Material):

    def __init__(self,
        texture: Texture=None,
        bump_texture: Texture=None,
        custom_shader: str = None,
        properties: Dict={}) -> None:

        if custom_shader == None:
            vert_code, frag_code = ShaderUtils.loadShaderCode("planet_material")
        else:
            vert_code, frag_code = ShaderUtils.loadShaderCode(custom_shader)

        super().__init__(vert_code, frag_code)
        
        # add base uniforms
        self.addUniform("vec3", "u_color", [1.0, 1.0, 1.0])

        # add light uniforms
        self.addUniform("vec3", "u_ambientColor", [0.4, 0.4, 0.4])
        self.addUniform("vec3", "u_lightColor", [0.6, 0.6, 0.6])
        self.addUniform("vec3", "u_lightDirection", [-1, 0, 0])
        self.addUniform("vec3", "u_viewPosition", [0, 0, 0])
        self.addUniform("float", "u_specularStrength", 1)
        self.addUniform("float", "u_shininess", 1)

        # add texture uniforms
        self.addUniform("bool", "u_useTexture", 0)
        if texture == None:
            self.addUniform("bool", "u_useTexture", False)
        else:
            self.addUniform("bool", "u_useTexture", True)
            self.addUniform("sampler2D", "u_texture", [texture._TextureRef, 1])

        # add bumpmap uniforms
        if bump_texture == None:
            self.addUniform("bool", "u_useBumpTexture", False)
        else:
            self.addUniform("bool", "u_useBumpTexture", True)
            self.addUniform("sampler2D", "u_bumpTexture", [bump_texture._TextureRef, 2])
            self.addUniform("float", "u_bumpStrength", 1.0)

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