from OpenGL.GL import *
import numpy as np

class Attribute(object):

    def __init__(self, data_type, data) -> None:
        self._DataType = data_type
        self._Data = data
        self._BufferRef = glGenBuffers(1)
        self.uploadData()
    
    def uploadData(self) -> None:
        data = np.array(self._Data).astype(np.float32)
        glBindBuffer(GL_ARRAY_BUFFER, self._BufferRef)
        glBufferData(GL_ARRAY_BUFFER, data.ravel(), GL_STATIC_DRAW)

    def associateVariable(self, variable_name, program_reference) -> None:
        variable_ref = glGetAttribLocation(program_reference, variable_name)

        if variable_ref != -1:
            glBindBuffer(GL_ARRAY_BUFFER, self._BufferRef)
            if self._DataType == "int":
                glVertexAttribPointer(variable_ref, 1, GL_INT, GL_FALSE, 0, None)
            elif self._DataType == "float":
                glVertexAttribPointer(variable_ref, 1, GL_FLOAT, GL_FALSE, 0, None)
            elif self._DataType == "vec2":
                glVertexAttribPointer(variable_ref, 2, GL_FLOAT, GL_FALSE, 0, None)
            elif self._DataType == "vec3":
                glVertexAttribPointer(variable_ref, 3, GL_FLOAT, GL_FALSE, 0, None)
            elif self._DataType == "vec4":
                glVertexAttribPointer(variable_ref, 4, GL_FLOAT, GL_FALSE, 0, None)
            else:
                raise Exception(f"Attribute {variable_name} has unknown type {self._DataType}")
            
            glEnableVertexAttribArray(variable_ref)