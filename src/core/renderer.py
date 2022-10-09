from typing import List
from OpenGL.GL import *
from core.mesh import Mesh
from core.scene import Scene
from core.camera import Camera
from core.uniform import Uniform

class Renderer(object):

    def __init__(self, clear_color = [0, 0, 0]) -> None:
        
        glEnable( GL_DEPTH_TEST )
        glEnable( GL_MULTISAMPLE )
        glClearColor(
            clear_color[0],
            clear_color[1],
            clear_color[2],
            1 )
        
        # for textures
        glEnable( GL_BLEND )
        glBlendFunc( GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA )

    def render(self, scene: Scene, camera: Camera) -> None:

        glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )

        camera.updateViewMatrix()

        descendant_list: List[object] = scene.getDescendantList()
        meshFilter = lambda x : isinstance(x, Mesh)
        mesh_list: List[Mesh] = list(filter(meshFilter, descendant_list))

        mesh: Mesh
        for mesh in mesh_list:

            # skip if mesh is not visible
            if not mesh._Visible:
                continue

            glUseProgram(mesh._Material._ProgramRef)

            # bind VAO (vertex arrat object)
            glBindVertexArray(mesh._VaoRef)

            # update uniforms outside material
            mesh._Material._Uniforms["u_model"]._Data = mesh.getWorldMatrix()
            mesh._Material._Uniforms["u_view"]._Data = camera._ViewMatrix
            mesh._Material._Uniforms["u_proj"]._Data = camera._ProjectionMatrix

            # update uniforms stored in material
            uniform_object: Uniform
            for variable_name, uniform_object in mesh._Material._Uniforms.items():
                uniform_object.uploadData()

            mesh._Material.updateRenderSettings()

            # render
            glDrawArrays(mesh._Material._Settings["drawStyle"], 0, mesh._Geometry._VertexCount)