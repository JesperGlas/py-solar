from typing import Tuple
from core.fileUtils import FileUtils

class ShaderUtils(object):

    @staticmethod
    def loadShaderCode(shader_name: str):
        shader_dir: str = FileUtils.getShaderDir(shader_name)
        print(shader_dir)
        with open(f"{shader_dir}/{shader_name}.vert", "r") as vert_file:
            vertex_shader_code: str = vert_file.read()
        with open(f"{shader_dir}/{shader_name}.frag") as frag_file:
            fragment_shader_code: str = frag_file.read()

        return ( vertex_shader_code, fragment_shader_code )