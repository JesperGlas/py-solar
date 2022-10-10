from OpenGL.GL import *
import pygame as pg

from core.mesh import Mesh
from core.uniform import Uniform
from core.scene import Scene
from core.camera import Camera
from light.light import Light
from light.shadow import Shadow


class Renderer:
    def __init__(self, clear_color=(0, 0, 0)):
        glEnable(GL_DEPTH_TEST)
        # required for antialiasing
        glEnable(GL_MULTISAMPLE)
        glClearColor(*clear_color, 1)
        self._window_size = pg.display.get_surface().get_size()
        self._ShadowsEnabled = False

    def render(self, scene: Scene, camera: Camera, clear_color=True, clear_depth=True, render_target=None):
        # filter descendents
        descendant_list = scene.getDescendantList()
        mesh_filter = lambda x: isinstance(x, Mesh)
        mesh_list = list(filter(mesh_filter, descendant_list))

        # shadow pass
        if self._ShadowsEnabled:
            # set render target properties
            glBindFramebuffer(GL_FRAMEBUFFER, self._ShadowObject._RenderTarget._FramebufferRef)
            glViewport(0, 0, self._ShadowObject._RenderTarget._Width, self._ShadowObject._RenderTarget._Height)

            # set default color to white, used when no objects present to cast shadows
            glClearColor(0, 0, 0, 1)
            glClear(GL_COLOR_BUFFER_BIT)
            glClear(GL_DEPTH_BUFFER_BIT)

            # everything in the scene gets rendered with depthMaterial so
            # only need to call glUseProgram & set matrices once
            glUseProgram(self._ShadowObject._Material._ProgramRef)
            self._ShadowObject.updateInternal()
            mesh: Mesh
            for mesh in mesh_list:
                # skip invisible meshes
                if not mesh._Visible:
                    continue
                # only triangle-based meshes cast shadows
                if mesh._Material._Settings["drawStyle"] != GL_TRIANGLES:
                    continue
                # bind VAO
                glBindVertexArray(mesh._VaoRef)
                # update transform data
                self._ShadowObject._Material._Uniforms["u_model"]._Data = mesh.getWorldMatrix()
                # update uniforms (matrix data) stored in shadow material
                uniform_object: Uniform
                for variable_name, uniform_object in self._ShadowObject._Material._Uniforms.items():
                    uniform_object.uploadData()
                glDrawArrays(GL_TRIANGLES, 0, mesh._Geometry._VertexCount)

        # activate render target
        if render_target is None:
            # set render target to window
            # (the value 0 is indicating the framebuffer attached to the window)
            glBindFramebuffer(GL_FRAMEBUFFER, 0)
            glViewport(0, 0, *self._window_size)
        else:
            # set render target properties
            glBindFramebuffer(GL_FRAMEBUFFER, render_target._FrameBufferRef)
            glViewport(0, 0, render_target._Width, render_target._Height)

        # clear color and depth buffers
        # glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        if clear_color:
            glClear(GL_COLOR_BUFFER_BIT)
        if clear_depth:
            glClear(GL_DEPTH_BUFFER_BIT)
        # blending
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        # Update camera view (calculate inverse)
        camera.updateViewMatrix()
        # Extract list of all Mesh instances in scene
        descendant_list = scene.getDescendantList()
        mesh_list = list(filter(lambda x: isinstance(x, Mesh), descendant_list))
        # Extract list of all Light instances in scene
        light_list = list(filter(lambda x: isinstance(x, Light), descendant_list))
        # Light list requires at least 4 lights due to shader structure
        while len(light_list) < 4: light_list.append( Light() )
        mesh: Mesh
        for mesh in mesh_list:
            # If this object is not visible, continue to next object in list
            if not mesh._Visible:
                continue
            glUseProgram(mesh._Material._ProgramRef)
            # Bind VAO
            glBindVertexArray(mesh._VaoRef)
            # Update uniform values stored outside of material
            mesh._Material._Uniforms["u_model"]._Data = mesh.getWorldMatrix()
            mesh._Material._Uniforms["u_view"]._Data = camera._ViewMatrix
            mesh._Material._Uniforms["u_proj"]._Data = camera._ProjectionMatrix
            # If material uses light data, add lights from list
            if "u_light0" in mesh._Material._Uniforms.keys():
                for light_number in range(4):
                    light_name = "u_light" + str(light_number)
                    light_instance = light_list[light_number]
                    mesh._Material._Uniforms[light_name]._Data = light_instance
            # Add camera position if needed (specular lighting)
            if "u_viewPosition" in mesh._Material._Uniforms.keys():
                mesh._Material._Uniforms["u_viewPosition"]._Data = camera.getWorldPosition()
            # Add shadow data if enabled and used by shader
            if self._ShadowsEnabled and "u_shadow0" in mesh._Material._Uniforms.keys():
                mesh._Material._Uniforms["u_shadow0"]._Data = self._ShadowObject
            # Update uniforms stored in material
            for uniform_object in mesh._Material._Uniforms.values():
                uniform_object.uploadData()
            # Update render settings
            mesh._Material.updateRenderSettings()
            glDrawArrays(mesh._Material._Settings["drawStyle"], 0, mesh._Geometry._VertexCount)

    def enableShadows(self, shadow_light, strength=0.5, resolution=(512, 512)):
        self._ShadowsEnabled = True
        self._ShadowObject = Shadow(shadow_light, strength=strength, resolution=resolution)
