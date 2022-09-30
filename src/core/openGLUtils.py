from OpenGL.GL import *

class OpenGLUtils(object):

    @staticmethod
    def initializeShader(shader_code, shader_type):
        
        shader_code = f"#version 330\n{shader_code}"
        shader_ref = glCreateShader(shader_type)
        glShaderSource(shader_ref, shader_code)
        glCompileShader(shader_ref)
        
        compile_success = glGetShaderiv(shader_ref, GL_COMPILE_STATUS)
        
        if not compile_success:
            error_message = glGetShaderInfoLog(shader_ref)
            glDeleteShader(shader_ref)
            error_message = f"\n{error_message.decode('utf-8')}"
            raise Exception(error_message)
        
        # link successful
        return shader_ref
    
    @staticmethod
    def initializeProgram(vertex_shader_code, fragment_shader_code):
        vertex_shader_ref = OpenGLUtils.initializeShader(vertex_shader_code, GL_VERTEX_SHADER)
        fragment_shader_ref = OpenGLUtils.initializeShader(fragment_shader_code, GL_FRAGMENT_SHADER)
        
        # create program and save reference
        program_ref = glCreateProgram()
        
        # attach shaders to program
        glAttachShader(program_ref, vertex_shader_ref)
        glAttachShader(program_ref, fragment_shader_ref)
        
        # link program
        glLinkProgram(program_ref)
        
        link_success = glGetProgramiv(program_ref, GL_LINK_STATUS)
        
        if not link_success:
            # get error message
            error_msg = glGetProgramInfoLog(program_ref)
            # free memory used by program
            glDeleteProgram(program_ref)
            # convert byte string to character string
            error_msg = f"\n{error_msg.decode('utf-8')}"
            # raise exception
            raise Exception(error_msg)

        # link successful
        return program_ref
    
    @staticmethod
    def printSystemInfo():
        print(f"Vendor: {glGetString(GL_VENDOR).decode('utf-8')}")
        print(f"Renderer: {glGetString(GL_RENDERER).decode('utf-8')}")
        print(f"OpenGL version supported: {glGetString(GL_VERSION).decode('utf-8')}")
        print(f"GLSL version supported: {glGetString(GL_SHADING_LANGUAGE_VERSION).decode('utf-8')}")