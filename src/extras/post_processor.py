from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from core.render_target import RenderTarget
from geometry.geometry import Geometry

class PostProcessor(object):

    def __init__(self, renderer: Renderer, scene: Scene, camera: Camera, final_render_target: RenderTarget=None) -> None:

        self._Renderer = renderer

        self._SceneList = [ scene ]
        self._CameraList = [ camera ]
        self._RenderTargetList = [ final_render_target ]
        self._FinalRenderTarget = final_render_target
        self._OrthoCamera = Camera()
