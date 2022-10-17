# external imports
from math import pi

# core imports
from core.fileUtils import FileUtils as FU
from core.camera import Camera
from core.input import Input
from core.texture import Texture
from core.mesh import Mesh

# extras imports
from extras.movement_rig import MovementRig

# geometry
from geometry.sphere_geometry import SphereGeometry

# material imports
from material.texture_material import TextureMaterial

# stellar imports


class StellarCamera(MovementRig):

    def __init__(self, view_distance=100) -> None:
        super().__init__()

        self._Camera = Camera(aspect_ratio=1280/720, far=view_distance + 100)
        self.add(self._Camera)

        sky_geo = SphereGeometry(radius=view_distance, radius_segments=128, height_segments=64)
        sky_mat = TextureMaterial(texture=Texture(FU.getAsset("stars.jpg")))
        self._Skybox = Mesh(sky_geo, sky_mat)
        self.add(self._Skybox)

    def setMoveSpeed(self, units_per_second: float) -> None:
        self._UnitsPerSecond = units_per_second

    def update(self, input_object: Input, delta_time) -> None:
        move_amount     = self._UnitsPerSecond * delta_time
        rotate_amount   = self._DegreesPerSecond * (pi / 180) * delta_time

        # reset camera position and direction
        if input_object.isKeyUp("space"):
            self.resetCamera()

        if input_object.isKeyPressed(self.KEY_MOVE_FORWARDS):
            self.translate( 0, 0, -move_amount )     
        if input_object.isKeyPressed(self.KEY_MOVE_BACKWARDS):
            self.translate( 0, 0, move_amount ) 
        if input_object.isKeyPressed(self.KEY_MOVE_LEFT):
            #self.translate( -move_amount, 0, 0 )
            self.rotateY(-rotate_amount, False)
            self._Skybox.rotateY(rotate_amount, False) # compensate for camera movement
        if input_object.isKeyPressed(self.KEY_MOVE_RIGHT):
            #self.translate( move_amount, 0, 0 ) 
            self.rotateY(rotate_amount, False)
            self._Skybox.rotateY(-rotate_amount, False) # compensate for camera movement
        if input_object.isKeyPressed(self.KEY_MOVE_UP):
            #self.translate( 0, move_amount, 0 )
            self.rotateX(rotate_amount, False)
            self._Skybox.rotateX(-rotate_amount, False)
        if input_object.isKeyPressed(self.KEY_MOVE_DOWN):
            #self.translate( 0, -move_amount, 0 ) 
            self.rotateX(-rotate_amount, False)
            self._Skybox.rotateX(rotate_amount, False)
        if input_object.isKeyPressed(self.KEY_TURN_RIGHT):
            self.rotateY( -rotate_amount ) 
            self._Skybox.rotateY(rotate_amount)
        if input_object.isKeyPressed(self.KEY_TURN_LEFT):
            self.rotateY( rotate_amount ) 
            self._Skybox.rotateY(-rotate_amount)
        if input_object.isKeyPressed(self.KEY_LOOK_UP):
            self._LookAttachment.rotateX( rotate_amount ) 
            self._Skybox.rotateX(-rotate_amount)
        if input_object.isKeyPressed(self.KEY_LOOK_DOWN):
            self._LookAttachment.rotateX( -rotate_amount )
            self._Skybox.rotateX(rotate_amount)

    def resetCamera(self, position=[0, 0, 5], direction=[0, 0, -1]) -> None:
        self.setPosition(position)
        self.setDirection(direction)