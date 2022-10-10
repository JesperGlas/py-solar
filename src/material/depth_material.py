from material.material import Material

class DepthMaterial(Material):

    def __init__(self) -> None:

        vert_code: str = """
        in vec3 a_position;
        uniform mat4 u_proj;
        uniform mat4 u_view;
        uniform mat4 u_model;

        void main()
        {
            gl_Position = u_proj * u_view * u_model * vec4(a_position, 1.0);
        }
        """

        frag_code: str = """
        out vec4 fragColor;

        void main()
        {
            float z = gl_FragCoord.z;
            fragColor = vec4(z, z, z, 1);
        }
        """
        super().__init__(vert_code, frag_code)
        self.locateUniforms()