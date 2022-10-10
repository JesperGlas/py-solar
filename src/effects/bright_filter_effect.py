from material.material import Material

class BrightFilterEffect(Material):

    def __init__(self, thresh_hold: float=2.4) -> None:

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
        uniform float u_threshHold;
        out vec4 fragColor;

        void main()
        {
            vec4 color = texture2D(u_texture, v_texCoords);
            if (color.r + color.g + color.b < u_threshHold)
                discard;
            fragColor = color;
        }
        """
        
        super().__init__(vert_code, frag_code)
        self.addUniform("sampler2D", "u_texture", [None, 1])
        self.addUniform("float", "u_threshHold", thresh_hold)
        self.locateUniforms()