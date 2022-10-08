from OpenGL.GL import *
from core.base import Base
from core.utils import OpenGLUtils as util
from core.attribute import Attribute
from core.uniform import Uniform
from core.matrix import Matrix
from core.input import Input
from math import pi


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
        uniform mat4 u_proj;
        uniform mat4 u_model;
        
        void main()
        {
            gl_Position = u_proj * u_model * vec4(a_position, 1.0);
        }
        """

        fs = """
        out vec4 fragColor;

        void main()
        {
            fragColor = vec4(1.0, 1.0, 0.0, 1.0);
        }
        """

        self._ProgramRef = util.initializeProgram(vs, fs)

        # render settings
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glEnable(GL_DEPTH_TEST)

        # vao
        vao_ref = glGenVertexArrays(1)
        glBindVertexArray(vao_ref)

        # attributes
        position_data = [
            [0.0, 0.2, 0.0],
            [0.1, -0.2, 0.0],
            [-0.1, -0.2, 0.0]
        ]
        self._VertexCount = len(position_data)

        a_position = Attribute("vec3", position_data)
        a_position.associateVariable("a_position", self._ProgramRef)

        # uniforms
        m_matrix = Matrix.makeTranslation(0, 0, -1)
        self._ModelMatrix = Uniform("mat4", m_matrix)
        self._ModelMatrix.locateVariable("u_model", self._ProgramRef)

        p_matrix = Matrix.makePerspective()
        self._ProjMatrix = Uniform("mat4", p_matrix)
        self._ProjMatrix.locateVariable("u_proj", self._ProgramRef)

        self._MoveSpeed = 0.5
        self._TurnSpeed = 90 * (pi/180)

    def update(self) -> None:
        move_amount = self._MoveSpeed * self._DeltaTime
        turn_amount = self._TurnSpeed * self._DeltaTime

        if self._Input.isKeyPressed("w"):
            m = Matrix.makeTranslation(0, move_amount, 0)
            self._ModelMatrix._Data = m @ self._ModelMatrix._Data
        if self._Input.isKeyPressed("s"):
            m = Matrix.makeTranslation(0, -move_amount, 0)
            self._ModelMatrix._Data = m @ self._ModelMatrix._Data
        if self._Input.isKeyPressed("a"):
            m = Matrix.makeTranslation(-move_amount, 0, 0)
            self._ModelMatrix._Data = m @ self._ModelMatrix._Data
        if self._Input.isKeyPressed("d"):
            m = Matrix.makeTranslation(move_amount, 0, 0)
            self._ModelMatrix._Data = m @ self._ModelMatrix._Data
        if self._Input.isKeyPressed("z"):
            m = Matrix.makeTranslation(0, 0, move_amount)
            self._ModelMatrix._Data = m @ self._ModelMatrix._Data
        if self._Input.isKeyPressed("x"):
            m = Matrix.makeTranslation(0, 0, -move_amount)
            self._ModelMatrix._Data = m @ self._ModelMatrix._Data
        if self._Input.isKeyPressed("q"):
            m = Matrix.makeRotationZ(turn_amount)
            self._ModelMatrix._Data = m @ self._ModelMatrix._Data
        if self._Input.isKeyPressed("e"):
            m = Matrix.makeRotationZ(-turn_amount)
            self._ModelMatrix._Data = m @ self._ModelMatrix._Data
        if self._Input.isKeyPressed("i"):
            m = Matrix.makeTranslation(0, move_amount, 0)
            self._ModelMatrix._Data = self._ModelMatrix._Data @ m
        if self._Input.isKeyPressed("k"):
            m = Matrix.makeTranslation(0, -move_amount, 0)
            self._ModelMatrix._Data = self._ModelMatrix._Data @ m
        if self._Input.isKeyPressed("j"):
            m = Matrix.makeTranslation(-move_amount, 0, 0)
            self._ModelMatrix._Data = self._ModelMatrix._Data @ m
        if self._Input.isKeyPressed("l"):
            m = Matrix.makeTranslation(move_amount, 0, 0)
            self._ModelMatrix._Data = self._ModelMatrix._Data @ m
        if self._Input.isKeyPressed("u"):
            m = Matrix.makeRotationZ(turn_amount)
            self._ModelMatrix._Data = self._ModelMatrix._Data @ m
        if self._Input.isKeyPressed("o"):
            m = Matrix.makeRotationZ(-turn_amount)
            self._ModelMatrix._Data = self._ModelMatrix._Data @ m

        # render scene
        glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
        glUseProgram(self._ProgramRef)

        self._ProjMatrix.uploadData()
        self._ModelMatrix.uploadData()
        
        glDrawArrays(GL_TRIANGLES, 0, self._VertexCount)
    
if __name__ == '__main__':
    App().run()