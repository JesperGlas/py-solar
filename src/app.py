from pathlib import Path

# core
from core.utils import OpenGLUtils
from core.base import Base
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from core.texture import Texture
from light.ambient_light import AmbientLight
from light.directional_light import DirectionalLight
from material.lambert_material import LambertMaterial
from geometry.sphere_geometry import SphereGeometry
from geometry.rectangle_geometry import RectangleGeometry
from extras.movement_rig import MovementRig


TITLE: str = "Solarpy"
VERSION: str = "1.0.0"
AUTHOR: str = "Jesper Glas"

class App(Base):

    def __init__(self, screen_size=[1280, 720], caption="App Window"):
        super().__init__(screen_size, caption)

        # print system information
        print(f"\nSystem information:")
        OpenGLUtils.printSystemInfo()

        # set up assets path
        self._Assets = f"{Path(__file__).resolve().parent}/assets"
        print(f"Assets path set to: {self._Assets}")

    def initialize(self) -> None:
        self.renderer = Renderer([0.2, 0.2, 0.2])
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=1280/720)
        self.rig = MovementRig()
        self.rig.add(self.camera)
        self.rig.setPosition([0, 2, 5])

        amb_light = AmbientLight(color=[0.2, 0.2, 0.2])
        self.scene.add(amb_light)

        self.dir_light = DirectionalLight(direction=[-1, -1, 0])
        self.dir_light.setPosition([2, 4, 0])
        self.scene.add(self.dir_light)

        geo = SphereGeometry()
        tex = Texture(f"{self._Assets}/earth.jpg")
        earth_mat = LambertMaterial( texture=tex, use_shadows=True)

        sp1 = Mesh(geo, earth_mat)
        sp1.setPosition([-2, 1, 0])
        self.scene.add(sp1)

        sp2 = Mesh(geo, earth_mat)
        sp2.setPosition([1, 2.2, -0.5])
        self.scene.add(sp2)

        self.renderer.enableShadows(self.dir_light)
        
    def update(self) -> None:
        self.dir_light.rotateY(0.01337, False)
        self.rig.update(self._Input, self._DeltaTime)
        self.renderer.render(self.scene, self.camera)
    
App().run()