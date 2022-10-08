from OpenGL.GL import *
from core.base import Base
from core.utils import OpenGLUtils as util
from core.attribute import Attribute
from core.uniform import Uniform

TITLE: str = "Solarpy"
VERSION: str = "1.0.0"
AUTHOR: str = "Jesper Glas"

class App(Base):

    def __init__(self, screen_size=[1280, 720], caption="Main Window"):
        super().__init__(screen_size, caption)

        # print system information
        print(f"\nSystem information:")
        util.printSystemInfo()

    def initialize(self) -> None:
        
        vs = """
        in vec3 a_position;
        uniform vec3 u_translation;

        void main()
        {
            vec3 pos = a_position + u_translation;
            gl_Position = vec4(pos.x, pos.y, pos.z, 1.0);
        }
        """

        fs = """
        uniform vec3 u_color;
        out vec4 fragColor;

        void main()
        {
            fragColor = vec4(u_color.r, u_color.g, u_color.b, 1.0);
        }
        """

        self._ProgramRef = util.initializeProgram(vs, fs)

        glClearColor(0.0, 0.0, 0.0, 1.0)
        
        vao_ref = glGenVertexArrays(1)
        glBindVertexArray(vao_ref)

        position_data = [
            [0.0, 0.2, 0.0],
            [0.2, -0.2, 0.0],
            [-0.2, -0.2, 0.0]
        ]
        self._VertexCount = len(position_data)
        a_position = Attribute("vec3", position_data)
        a_position.associateVariable("a_position", self._ProgramRef)

        self._Trans = Uniform("vec3", [-0.5, 0.0, 0.0])
        self._Trans.locateVariable("u_translation", self._ProgramRef)

        self._Color = Uniform("vec3", [1.0, 0.0, 0.0])
        self._Color.locateVariable("u_color", self._ProgramRef)

    def update(self) -> None:

        self._Trans._Data[0] += 0.01
        if self._Trans._Data[0] > 1.2:
            self._Trans._Data[0] = -1.2

        glClear(GL_COLOR_BUFFER_BIT)

        glUseProgram(self._ProgramRef)
        self._Trans.uploadData()
        self._Color.uploadData()
        glDrawArrays(GL_TRIANGLES, 0, self._VertexCount)
    
if __name__ == '__main__':
    App().run()