from material.material import Material

class HorizontalBlurEffect(Material):

    def __init__(self, texture_size=[512, 512], blur_radius=20) -> None:

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
        uniform vec2 u_textureSize;
        uniform int u_blurRadius;
        out vec4 fragColor;

        void main()
        {
            vec2 pixel_to_tex_coord = 1 / u_textureSize;
            vec4 avg_color = vec4(0, 0, 0, 0);
            for (int offset_x = -u_blurRadius; offset_x <= u_blurRadius; offset_x++)
            {
                float weight = u_blurRadius - abs(offset_x) + 1;
                vec2 offset_tex_coord = vec2(offset_x, 0) * pixel_to_tex_coord;
                avg_color += texture2D(u_texture, v_texCoords + offset_tex_coord) * weight;
            }
            avg_color /= avg_color.a;

            fragColor = avg_color;
        }
        """
        
        super().__init__(vert_code, frag_code)
        self.addUniform("sampler2D", "u_texture", [None, 1])
        self.addUniform("vec2", "u_textureSize", texture_size)
        self.addUniform("int", "u_blurRadius", blur_radius)
        self.locateUniforms()