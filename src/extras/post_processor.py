from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from core.render_target import RenderTarget
from geometry.geometry import Geometry
from effects.template_effect import TemplateEffect

class PostProcessor(object):

    def __init__(self, renderer: Renderer, scene: Scene, camera: Camera, final_render_target: RenderTarget=None) -> None:

        self._Renderer = renderer

        self._SceneList = [ scene ]
        self._CameraList = [ camera ]
        self._RenderTargetList = [ final_render_target ]
        self._FinalRenderTarget = final_render_target
        self._OrthoCamera = Camera()
        self._OrthoCamera.setOrthographic() # aligned with clip space

        # generate rectangle aligned with clip space
        self._RectangleGeometry = Geometry()
        p0, p1, p2, p3 = [-1, -1], [1, -1], [-1, 1], [1, 1]
        t0, t1, t2, t3 = [ 0,  0], [1,  0], [ 0, 1], [1, 1]
        position_data = [ p0, p1, p3, p0, p3, p2 ]
        texture_data =  [ t0, t1, t3, t0, t3, t2 ]
        self._RectangleGeometry.addAttribute("vec2", "a_position", position_data)
        self._RectangleGeometry.addAttribute("vec2", "a_texCoords", texture_data)
        self._RectangleGeometry.countVertecies()

    def addEffect(self, effect: TemplateEffect):

        post_scene = Scene()
        resolution = self._Renderer._WindowSize
        target = RenderTarget( resolution )

        # change
        self._RenderTargetList[-1] = target

        effect._Uniforms["u_texture"]._Data[0] = target._Texture._TextureRef

        mesh = Mesh( self._RectangleGeometry, effect )
        post_scene.add( mesh )

        self._SceneList.append( post_scene )
        self._CameraList.append( self._OrthoCamera )
        self._RenderTargetList.append( self._FinalRenderTarget )

    def render(self) -> None:
        passes = len( self._SceneList )
        for n in range( passes ):
            scene = self._SceneList[n]
            camera = self._CameraList[n]
            target = self._RenderTargetList[n]
            self._Renderer.render( scene, camera, render_target=target)