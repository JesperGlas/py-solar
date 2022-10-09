from typing import Dict
from OpenGL.GL import *
from material.material import Material
from core.texture import Texture

class TextureMaterial(Material):
    
    def __init__(self, texture: Texture, properties: Dict={}) -> None:

        vs_code: str = """
        uniform mat4 u_proj;
        uniform mat4 u_view;
        uniform mat4 u_model;
        in vec3 a_position;
        in vec2 a_texCoords;
        uniform vec2 u_texRepeat;
        uniform vec2 u_texOffset;
        out vec2 v_texCoords;

        void main()
        {
            gl_Position = u_proj * u_view * u_model * vec4(a_position, 1.0);
            v_texCoords = a_texCoords * u_texRepeat + u_texOffset;
        }
        """

        fs_code: str = """
        uniform vec3 u_color;
        uniform sampler2D u_texture;
        in vec2 v_texCoords;
        out vec4 fragColor;

        void main()
        {
            vec4 color = vec4(u_color, 1.0) * texture2D(u_texture, v_texCoords);
            if (color.a < 0.1)
                discard;

            fragColor = color;
        }
        """

        super().__init__(vs_code, fs_code)

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