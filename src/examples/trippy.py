from core.utils import OpenGLUtils
from core.base import Base
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from material.material import Material
from geometry.sphere_geometry import SphereGeometry

TITLE: str = "Solarpy"
VERSION: str = "1.0.0"
AUTHOR: str = "Jesper Glas"

class App(Base):

    def __init__(self, screen_size=[1280, 720], caption="Main Window"):
        super().__init__(screen_size, caption)

        # print system information
        print(f"\nSystem information:")
        OpenGLUtils.printSystemInfo()

    def initialize(self) -> None:
        self._Renderer = Renderer()
        self._Scene = Scene()
        self._Camera = Camera(aspect_ratio=1280/720)
        
        # set camera position
        self._Camera.setPosition([0, 0, 7])

        vs_code: str = """
        uniform mat4 u_model;
        uniform mat4 u_view;
        uniform mat4 u_proj;
        uniform float u_time;
        in vec3 a_position;
        in vec3 a_color;
        out vec3 v_color;

        void main()
        {
            float offset = 0.2 * sin(8.0 * a_position.x + u_time);
            vec3 pos = a_position + vec3(0.0, offset, 0.0);

            gl_Position = u_proj * u_view * u_model * vec4(pos, 1.0);
            v_color = a_color;
        }
        """

        fs_code: str = """
        in vec3 v_color;
        uniform float u_time;
        out vec4 fragColor;

        void main()
        {
            float r = abs(sin(u_time));
            vec4 c = vec4(r, -0.5*r, -0.5*r, 0.0);
            fragColor = vec4(v_color, 1.0) + c;
        }
        """

        material = Material(vs_code, fs_code)
        material.addUniform("float", "u_time", 0)
        material.locateUniforms()

        geometry = SphereGeometry(3, 128, 64)

        self._ElapsedTime = 0
        self._Mesh = Mesh(geometry, material)
        self._Scene.add(self._Mesh)

    def update(self) -> None:
        # update uniforms
        self._ElapsedTime += 1/60
        self._Mesh._Material._Uniforms["u_time"]._Data = self._ElapsedTime

        # render
        self._Renderer.render(self._Scene, self._Camera)
    
App().run()