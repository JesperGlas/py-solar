from core.base import Base
from core.openGLUtils import OpenGLUtils
from OpenGL.GL import *

class Test(Base):
    
    def initilize(self) -> None:
        print("Init program...")
        
        # vertex shader
        vert_code = """
        void main()
        {
            gl_Position = vec4(0.0, 0.0, 0.0, 1.0);
        }
        """
        
        # fragment shader
        frag_code = """
        out vec4 fragColor;
        void main()
        {
            fragColor = vec4(1.0, 1.0, 0.0, 1.0);
        }
        """
        
        # send code to GPU - compile - store - reference
        self.program_ref = OpenGLUtils.initializeProgram(vert_code, frag_code)
        
        # set vert arrat obj
        vao_ref = glGenVertexArrays(1)
        glBindVertexArray(vao_ref)
        
        # render settings (optional)
        glPointSize(10)
        
        return super().initilize()

    def update(self) -> None:
        # select program for rendering
        glUseProgram(self.program_ref)
        
        # render geometric objects using selected programs
        glDrawArrays(GL_POINTS, 0, 1)
        return super().update()

Test().run()