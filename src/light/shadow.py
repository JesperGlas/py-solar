from OpenGL.GL import *
from core.camera import Camera
from core.render_target import RenderTarget
from material.depth_material import DepthMaterial

class Shadow(object):

    def __init__(self,
        light_source,
        strength=0.5,
        resolution=[512, 512],
        camera_bounds=[-5, 5, -5, 5, 0, 100],
        bias=0.1
        ) -> None:

        # Must be directional
        self._LightSource = light_source

        # camera used to render scene from light source perspective
        self._Camera = Camera()
        l, r, b, t, n, f = camera_bounds
        self._Camera.setOrthographic(l, r, b, t, n, f)
        self._LightSource.add(self._Camera)
        self._RenderTarget = RenderTarget(
            resolution,
            properties={"wrap": GL_CLAMP_TO_BORDER } )
        self._Material = DepthMaterial()
        self._Strength = strength
        self._Bias = bias

    def updateInternal(self) -> None:
        self._Camera.updateViewMatrix()
        self._Material._Uniforms["u_view"]._Data = self._Camera._ViewMatrix
        self._Material._Uniforms["u_proj"]._Data = self._Camera._ProjectionMatrix
