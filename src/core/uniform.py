from OpenGL.GL import *
from light.light import Light


class Uniform(object):

    def __init__(self, data_type, data) -> None:
        # allowed data types:
        # int | bool | float | vec2 | vec3 | vec4 | mat4 | sampler2D | Light
        self._DataType = data_type
        self._Data = data

        self._VariableRef = None

    def locateVariable(self, variable_name, program_ref) -> None:
        if self._DataType == "Light":
            self._VariableRef = {}
            self._VariableRef["lightType"] = glGetUniformLocation(
                program_ref, f"{variable_name}.lightType" )
            self._VariableRef["color"] = glGetUniformLocation(
                program_ref, f"{variable_name}.color" )
            self._VariableRef["direction"] = glGetUniformLocation(
                program_ref, f"{variable_name}.direction" )
            self._VariableRef["position"] = glGetUniformLocation(
                program_ref, f"{variable_name}.position" )
            self._VariableRef["attenuation"] = glGetUniformLocation(
                program_ref, f"{variable_name}.attenuation" )
        elif self._DataType == "Shadow":
            self._VariableRef = {}
            self._VariableRef["lightDirection"] = glGetUniformLocation(
                program_ref, f"{variable_name}.lightDirection" )
            self._VariableRef["projection"] = glGetUniformLocation(
                program_ref, f"{variable_name}.projection" )
            self._VariableRef["view"] = glGetUniformLocation(
                program_ref, f"{variable_name}.view" )
            self._VariableRef["depthTexture"] = glGetUniformLocation(
                program_ref, f"{variable_name}.depthTexture" )
            self._VariableRef["strength"] = glGetUniformLocation(
                program_ref, f"{variable_name}.strength" )
            self._VariableRef["bias"] = glGetUniformLocation(
                program_ref, f"{variable_name}.bias" )
        else:
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
        elif self._DataType == "Light":
            self._Data: Light
            glUniform1i( self._VariableRef["lightType"], self._Data._LightType )
            glUniform3f( self._VariableRef["color"], *self._Data._LightColor )
            glUniform3f( self._VariableRef["direction"], *self._Data.getDirection() )
            glUniform3f( self._VariableRef["position"], *self._Data.getPosition() )
            glUniform3f( self._VariableRef["attenuation"], *self._Data._Attenuation )
        elif self._DataType == "Shadow":
            glUniform3f(
                self._VariableRef["lightDirection"],
                *self._Data._LightSource.getDirection() )
            glUniformMatrix4fv(
                self._VariableRef["projection"],
                1, GL_TRUE, self._Data._Camera._ViewMatrix )
            texture_object_ref = self._Data._RenderTarget._Texture._TextureRef
            texture_unit_ref = 15
            glActiveTexture( GL_TEXTURE0 + texture_unit_ref )
            glBindTexture( GL_TEXTURE_2D, texture_object_ref )
            glUniform1i( self._VariableRef["depthTexture"], texture_unit_ref )
            glUniform1f( self._VariableRef["strength"], self._Data._Strength )
            glUniform1f( self._VariableRef["bias"], self._Data._Bias )
        else:
            raise Exception(f"Unrecognized uniform type: {self._DataType}")