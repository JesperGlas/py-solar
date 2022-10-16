from typing import Dict
from OpenGL.GL import *
from core.fileUtils import FileUtils
from shaders.shaderUtils import ShaderUtils
from material.material import Material
from core.texture import Texture

class OrbitalMaterial(Material):

    def __init__(self,
        color_tex_name: str=None,
        bump_tex_name: str=None,
        atmosphere_tex_name: str=None,
        night_tex_name: str=None,
        custom_shader: str = None,
        use_shadows: bool=False,
        properties: Dict={}) -> None:

        if custom_shader == None:
            vert_code, frag_code = ShaderUtils.loadShaderCode("orbital_shader")
        else:
            vert_code, frag_code = ShaderUtils.loadShaderCode(custom_shader)

        super().__init__(vert_code, frag_code)
        
        # add base uniforms
        self.addUniform("vec3", "u_color", [1.0, 1.0, 1.0])
        self.addUniform("float", "u_time", 0)

        # light uniforms
        self.addUniform("Light", "u_light", None)
        self.addUniform("vec3", "u_viewPosition", [0, 0, 0])
        self.addUniform("vec3", "u_objectPosition", [0, 0, 0])

        for n in range(2):
            self.addUniform("Occluder", f"u_occluder{n}", None)
        
        # add shadow uniforms

        # add texture uniforms
        self.addUniform("bool", "u_useTexture", 0)
        if color_tex_name == None:
            self.addUniform("bool", "u_useTexture", False)
        else:
            color_texture = Texture(FileUtils.getAsset(color_tex_name))
            self.addUniform("bool", "u_useTexture", True)
            self.addUniform("sampler2D", "u_texture", [color_texture._TextureRef, 1])

        # add bumpmap uniforms
        if bump_tex_name == None:
            self.addUniform("bool", "u_useBumpTexture", False)
        else:
            bump_texture = Texture(FileUtils.getAsset(bump_tex_name))
            self.addUniform("bool", "u_useBumpTexture", True)
            self.addUniform("sampler2D", "u_bumpTexture", [bump_texture._TextureRef, 2])
            self.addUniform("float", "u_bumpStrength", 1.0)

        # atmospheric effect
        if atmosphere_tex_name == None:
            self.addUniform("bool", "u_useAtmosphere", False)
        else:
            atmosphere_texture = Texture(FileUtils.getAsset(atmosphere_tex_name))
            self.addUniform("bool", "u_useAtmosphere", True)
            self.addUniform("sampler2D", "u_atmosphereTexture", [atmosphere_texture._TextureRef, 3])

        if night_tex_name == None:
            self.addUniform("bool", "u_useNightTexture", False)
        else:
            night_texture = Texture(FileUtils.getAsset(night_tex_name))
            self.addUniform("bool", "u_useNightTexture", True)
            self.addUniform("sampler2D", "u_nightTexture", [night_texture._TextureRef, 4])

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