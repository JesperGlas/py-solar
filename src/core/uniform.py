from OpenGL.GL import *

class Uniform(object):

    def __init__(self, data_type, data) -> None:
        # allowed data types:
        # int | bool | float | vec2 | vec3 | vec4
        self._DataType = data_type
        self._Data = data

        self._VariableRef = None

    def locateVariable(self, variable_name, program_ref) -> None:
        self._VariableRef = glGetUniformLocation(program_ref, variable_name)

    # should this be intended?
    def uploadData(self) -> None:

        # if variable does not exist; return
        if self._VariableRef == -1:
            return

        # else;
        if self._DataType == "int":
            glUniform1i(self._VariableRef, self._Data)
        elif self._DataType == "bool":
            glUniform1i(self._VariableRef, self._Data)
        elif self._DataType == "float":
            glUniform1f(self._VariableRef, self._Data)
        elif self._DataType == "vec2":
            glUniform2f(self._VariableRef, *self._Data)
        elif self._DataType == "vec3":
            glUniform3f(self._VariableRef, *self._Data)
        elif self._DataType == "vec4":
            glUniform4f(self._VariableRef, *self._Data)
        elif self._DataType == "mat4":
            glUniformMatrix4fv(self._VariableRef, 1, GL_TRUE, self._Data)
        elif self._DataType == "sampler2D":
            texture_object_ref, texture_unit_ref = self._Data
            # activate texture unit
            glActiveTexture( GL_TEXTURE0 + texture_unit_ref )
            # associate texture object reference to currently
            #   active texture unit
            glBindTexture( GL_TEXTURE_2D, texture_object_ref )
            # upload texture unit number (0, ..., 15) to
            #   uniform variable in shader
            glUniform1i( self._VariableRef, texture_unit_ref )
        else:
            raise Exception(f"Unrecognized uniform type: {self._DataType}")