from OpenGL.GL import *
from core.base import Base
from core.utils import OpenGLUtils as util
from core.attribute import Attribute

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
        in vec3 a_color;
        out vec3 v_color;

        void main()
        {
            gl_Position = vec4(a_position, 1.0);
            v_color = a_color;
        }
        """

        fs = """
        in vec3 v_color;
        out vec4 fragColor;

        void main()
        {
            fragColor = vec4(v_color, 1.0);
        }
        """

        self._ProgramRef = util.initializeProgram(vs, fs)
        glLineWidth(4)
        glPointSize(10)

        vao_ref = glGenVertexArrays(1)
        glBindVertexArray(vao_ref)

        position_data = [
            [0.8, 0.0, 0.0],    [0.4, 0.6, 0.0],
            [-0.4, 0.6, 0.0],   [-0.8, 0.0, 0.0],
            [-0.4, -0.6, 0.0],  [0.4, -0.6, 0.0]
        ]

        self._VertexCount = len(position_data)
        position_attribute = Attribute("vec3", position_data)
        position_attribute.associateVariable("a_position", self._ProgramRef)

        color_data = [
            [1.0, 0.0, 0.0], [1.0, 0.5, 0.0],
            [1.0, 1.0, 1.0], [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0], [0.5, 0.0, 1.0]
        ]

        color_attribute = Attribute("vec3", color_data)
        color_attribute.associateVariable("a_color", self._ProgramRef)

    def update(self) -> None:
        glUseProgram(self._ProgramRef)
        glDrawArrays(GL_POINTS, 0, self._VertexCount)
    
if __name__ == '__main__':
    App().run()