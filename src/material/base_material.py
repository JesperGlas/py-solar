from material.material import Material
from core.uniform import Uniform

class BaseMaterial(Material):

    def __init__(self) -> None:

        vert_code: str = """
        uniform mat4 u_proj;
        uniform mat4 u_view;
        uniform mat4 u_model;
        in vec3 a_position;
        in vec3 a_color;
        out vec3 v_color;

        void main()
        {
            gl_Position = u_proj * u_view * u_model * vec4(a_position, 1.0);
            v_color = a_color;
        }
        """

        frag_code: str = """
        uniform vec3 u_color;
        uniform bool u_useVertexColors;
        in vec3 v_color;
        out vec4 fragColor;

        void main()
        {
            vec4 tempColor = vec4(u_color, 1.0);

            if (u_useVertexColors)
                tempColor *= vec4(v_color, 1.0);

            fragColor = tempColor;
        }
        """

        super().__init__(vert_code, frag_code)
        self.addUniform("vec3", "u_color", [1.0, 1.0, 1.0])
        self.addUniform("bool", "u_useVertexColors", False)
        self.locateUniforms()