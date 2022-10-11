from math import pi
from pathlib import Path
from typing import Dict

# core
from core.openGLUtils import OpenGLUtils
from core.fileUtils import FileUtils
from core.base import Base
from core.renderer import Renderer

# scene
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh

# geometry
from geometry.sphere_geometry import SphereGeometry
from geometry.rectangle_geometry import RectangleGeometry

# material
from material.lambert_material import LambertMaterial
from material.phong_material import PhongMaterial
from material.surface_material import SurfaceMaterial

# texture
from core.texture import Texture
from material.texture_material import TextureMaterial

# extra
from extras.movement_rig import MovementRig
from extras.post_processor import PostProcessor

# light
from light.ambient_light import AmbientLight
from light.directional_light import DirectionalLight

TITLE: str = "Solarpy"
VERSION: str = "1.0.0"
AUTHOR: str = "Jesper Glas"

class App(Base):

    def __init__(self, screen_size=[1280, 720], caption="App Window"):
        super().__init__(screen_size, caption)

        # print system information
        print(f"\nSystem information:")
        OpenGLUtils.printSystemInfo()
        FileUtils.setProjectRoot()

    def initialize(self) -> None:
        self._Scene = Scene()
        self._Camera = Camera(aspect_ratio=1280/720)
        self._Renderer = Renderer(clear_color=[0, 0, 0])
        
        # setup moving camera position
        self._CameraRig = MovementRig()
        self._CameraRig.add(self._Camera)
        self._CameraRig.setPosition([0, 0, 8])
        self._Scene.add(self._CameraRig)

        # set up geometry
        sun_geo = SphereGeometry(radius=0.1)
        earth_geo = SphereGeometry(radius=2, radius_segments=64, height_segments=32)
        moon_geo = SphereGeometry(radius=0.5)

        # set up textures
        earth_tex = Texture(FileUtils.getAsset("earth.jpg"))
        moon_tex = Texture(FileUtils.getAsset("moon.jpg"))
        
        # bump maps
        earth_bump = Texture(FileUtils.getAsset("earth_bump.jpg"))
        moon_bump = Texture(FileUtils.getAsset("moon_bump.jpg"))

        # set up material
        sun_mat = SurfaceMaterial(properties={"u_color": [1, 0, 0]})
        earth_mat = LambertMaterial( texture=earth_tex, bump_texture=earth_bump, use_shadows=True )
        moon_mat = LambertMaterial( texture=moon_tex, bump_texture=moon_bump, use_shadows=True )

        # set up meshes
        self._Sun = Mesh(sun_geo, sun_mat)
        self._Sun.setPosition([0, 0, 10])
        #self._Scene.add(self._Sun)

        self._Earth = Mesh(earth_geo, earth_mat)
        self._Earth.setPosition([0, 0, 0])
        self._Scene.add(self._Earth)

        self._Moon = Mesh(moon_geo, moon_mat)
        self._Moon.setPosition([-3, 0, 3])
        self._Scene.add(self._Moon)

        # set up light
        self._Ambient = AmbientLight(color=[0.1, 0.1, 0.1])
        self._Scene.add(self._Ambient)
        self._SunLight = DirectionalLight(
            color=[0.8, 0.8, 0.8],
            direction=[0, 0, -1] )
        self._SunLight.setPosition([0, 0, 10])
        self._Scene.add(self._SunLight)

        # shadows
        self._Renderer.enableShadows( shadow_light=self._SunLight, strength=1, resolution=[1280, 720], bias=1 )

        # post processing
        
        # depth texture
        
        # optional: render depth texture to mesh in scene
        depth_texture = self._Renderer._ShadowObject._RenderTarget._Texture
        shadow_display = Mesh(RectangleGeometry(2, 2), TextureMaterial(depth_texture))
        shadow_display.setPosition([4, 0, 0])
        self._Scene.add(shadow_display)

        # scene info
        print(f"Scene info:")
        self._Scene.printNodeTree()
        
    def update(self) -> None:
        # update data
        self._CameraRig.update(self._Input, self._DeltaTime)
        if self._Input.isKeyPressed("space"):
            self._SunLight.rotateY(-0.02, False)

        self._Earth.rotateY(0.002, True)
        self._Moon.rotateY(0.002, True)
        
        # update uniforms

        # render
        self._Renderer.render(self._Scene, self._Camera)
        
        # render scene from shadow camera
        shadow_camera = self._Renderer._ShadowObject._Camera
        #self._Renderer.render(self._Scene, shadow_camera)
        
    
App().run()