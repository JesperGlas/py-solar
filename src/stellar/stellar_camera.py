from typing import overload
from math import pi
from core.fileUtils import FileUtils as FU
from stellar.stellar_utils import StellarUtils as SU
from core.camera import Camera
from core.input import Input
from extras.movement_rig import MovementRig

from geometry.sphere_geometry import SphereGeometry
from core.texture import Texture
from material.texture_material import TextureMaterial
from core.mesh import Mesh
from core.object3D import Object3D

class StellarCamera(MovementRig):

    def __init__(self, units_per_sec=1, degrees_per_sec=60, view_distance=1000) -> None:
        super().__init__(units_per_sec, degrees_per_sec)

        self._Camera = Camera(aspect_ratio=1280/720, far=SU.UNIT_RADIUS)
        self.add(self._Camera)

        sky_geo = SphereGeometry(radius=view_distance, radius_segments=128, height_segments=64)
        sky_mat = TextureMaterial(texture=Texture(FU.getAsset("stars.jpg")))
        self._Skybox = Mesh(sky_geo, sky_mat)
        self.add(self._Skybox)

    def setMoveSpeed(self, units_per_second: float) -> None:
        self._UnitsPerSecond = units_per_second

    def detach(self) -> None:
        if self._Parent:
            self._Parent.remove(self)

    def attach(self, target: Object3D, distance=1) -> None:
        if self._Parent:
            self.detach()
        target.add(self)
        self.setPosition([0, 0, distance])

    def update(self, input_object: Input, delta_time) -> None:
        move_amount     = self._UnitsPerSecond * delta_time
        rotate_amount   = self._DegreesPerSecond * (pi / 180) * delta_time

        if input_object.isKeyPressed(self. KEY_MOVE_FORWARDS):
            self.translate( 0, 0, -move_amount )     
        if input_object.isKeyPressed(self. KEY_MOVE_BACKWARDS):
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