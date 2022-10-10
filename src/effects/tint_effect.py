from material.material import Material

class TintEffect(Material):

    def __init__(self, tint_color=[1, 0, 0]) -> None:

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
        uniform vec3 u_tintColor;
        uniform sampler2D u_texture;
        out vec4 fragColor;

        void main()
        {
            vec4 color = texture2D(u_texture, v_texCoords);
            float gray = (color.r + color.g + color.b) / 3.0;
            fragColor = vec4(gray * u_tintColor, 1.0);
        }
        """
        
        super().__init__(vert_code, frag_code)
        self.addUniform("sampler2D", "u_texture", [None, 1])
        self.addUniform("vec3", "u_tintColor", tint_color)
        self.locateUniforms()