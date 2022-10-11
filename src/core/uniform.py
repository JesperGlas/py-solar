from OpenGL.GL import *
from light.light import Light

class Uniform(object):

    def __init__(self, data_type, data):
        # type of data:
        # int | bool | float | vec2 | vec3 | vec4
        self._DataType = data_type
        # data to be sent to uniform variable
        self._Data = data
        # reference for variable location in program
        self._VariableRef = None

    def locateVariable(self, variable_name: str, program_ref):
        """ Get and store reference for program variable with given name """
        if self._DataType == 'Light':
            self._VariableRef = {
                "lightType":    glGetUniformLocation(program_ref, f"{variable_name}.lightType"),
                "color":        glGetUniformLocation(program_ref, f"{variable_name}.color"),
                "direction":    glGetUniformLocation(program_ref, f"{variable_name}.direction"),
                "position":     glGetUniformLocation(program_ref, f"{variable_name}.position"),
                "attenuation":  glGetUniformLocation(program_ref, f"{variable_name}.attenuation"),
            }
        elif self._DataType == "Shadow":
            self._VariableRef = {
                "lightDirection":   glGetUniformLocation(program_ref, f"{variable_name}.lightDirection"),
                "projectionMatrix": glGetUniformLocation(program_ref, f"{variable_name}.projectionMatrix"),
                "viewMatrix":       glGetUniformLocation(program_ref, f"{variable_name}.viewMatrix"),
                "depthTexture":     glGetUniformLocation(program_ref, f"{variable_name}.depthTexture"),
                "strength":         glGetUniformLocation(program_ref, f"{variable_name}.strength"),
                "bias":             glGetUniformLocation(program_ref, f"{variable_name}.bias"),
            }
        else:
            self._VariableRef = glGetUniformLocation(program_ref, variable_name)

    def uploadData(self):
        """ Store data in uniform variable previously located """
        # if the program does not reference the variable, then exit
        if self._VariableRef != -1:
            if self._DataType == 'int':
                glUniform1i(self._VariableRef, self._Data)
            elif self._DataType == 'bool':
                glUniform1i(self._VariableRef, self._Data)
            elif self._DataType == 'float':
                glUniform1f(self._VariableRef, self._Data)
            elif self._DataType == 'vec2':
                glUniform2f(self._VariableRef, *self._Data)
            elif self._DataType == 'vec3':
                glUniform3f(self._VariableRef, *self._Data)
            elif self._DataType == 'vec4':
                glUniform4f(self._VariableRef, *self._Data)
            elif self._DataType == 'mat4':
                glUniformMatrix4fv(self._VariableRef, 1, GL_TRUE, self._Data)
            elif self._DataType == "sampler2D":
                texture_object_ref, texture_unit_ref = self._Data
                # activate texture unit
                glActiveTexture(GL_TEXTURE0 + texture_unit_ref)
                # associate texture object reference to currently active texture unit
                glBindTexture(GL_TEXTURE_2D, texture_object_ref)
                # upload texture unit number (0...15) to uniform variable in shader
                glUniform1i(self._VariableRef, texture_unit_ref)
            elif self._DataType == "Light":
                self._Data: Light
                glUniform1i(self._VariableRef["lightType"],     self._Data._LightType)
                glUniform3f(self._VariableRef["color"],         *self._Data._LightColor)
                glUniform3f(self._VariableRef["direction"],     *self._Data.getDirection())
                glUniform3f(self._VariableRef["position"],      *self._Data.getPosition())
                glUniform3f(self._VariableRef["attenuation"],   *self._Data._Attenuation)
            elif self._DataType == "Shadow":
                glUniform3f(self._VariableRef["lightDirection"],
                    *self._Data._LightSource.getDirection())
                glUniformMatrix4fv(self._VariableRef["projectionMatrix"],
                    1, GL_TRUE, self._Data._Camera._ProjectionMatrix)
                glUniformMatrix4fv(self._VariableRef["viewMatrix"],
                    1, GL_TRUE, self._Data._Camera._ViewMatrix)
                # Configure depth texture
                texture_object_ref = self._Data._RenderTarget._Texture._TextureRef
                texture_unit_ref = 15
                glActiveTexture(GL_TEXTURE0 + texture_unit_ref)
                glBindTexture(GL_TEXTURE_2D, texture_object_ref)
                glUniform1i(self._VariableRef["depthTexture"], texture_unit_ref)
                glUniform1f(self._VariableRef["strength"], self._Data._Strength)
                glUniform1f(self._VariableRef["bias"], self._Data._Bias)