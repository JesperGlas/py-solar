from material.material import Material
from core.texture import Texture

class AdditiveBlendEffect(Material):

    def __init__(self, blend_texture: Texture=None, original_strength=1, blend_strength=1) -> None:

        vert_code: str = """
        in vec2 a_position;
        in vec2 a_texCoords;
        out vec2 v_texCoords;

        void main()
        {
            gl_Position = vec4(a_position, 0.0, 1.0);
            v_texCoords = a_texCoords;
        }
        """

        frag_code: str = """
        in vec2 v_texCoords;
        uniform sampler2D u_texture;
        uniform sampler2D u_blendTexture;
        uniform float u_originalStrength;
        uniform float u_blendStrength;
        out vec4 fragColor;

        void main()
        {
            vec4 original_color = texture2D(u_texture, v_texCoords);
            vec4 blend_color = texture2D(u_blendTexture, v_texCoords);
            vec4 color =    u_originalStrength * original_color
                            + u_blendStrength * blend_color;
            fragColor = color;
        }
        """
        
        super().__init__(vert_code, frag_code)
        self.addUniform("sampler2D", "u_texture", [None, 1])
        self.addUniform("sampler2D", "u_blendTexture", [blend_texture._TextureRef, 2])
        self.addUniform("float", "u_originalStrength", original_strength)
        self.addUniform("float", "u_blendStrength", blend_strength)
        self.locateUniforms()