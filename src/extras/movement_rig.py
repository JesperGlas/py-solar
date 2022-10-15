from core.object3D import Object3D
from core.input import Input
from math import pi

class MovementRig(Object3D):

     def __init__(self, units_per_sec=1, degrees_per_sec=60) -> None:
          super().__init__()

          self._LookAttachment = Object3D()
          self._Children = [self._LookAttachment]
          self._LookAttachment._Parent = self

          self._UnitsPerSecond = units_per_sec
          self._DegreesPerSecond = degrees_per_sec

          # keymap
          self.KEY_MOVE_FORWARDS  = "w" 
          self.KEY_MOVE_BACKWARDS = "s" 
          self.KEY_MOVE_LEFT      = "a" 
          self.KEY_MOVE_RIGHT     = "d" 
          self.KEY_MOVE_UP        = "r" 
          self.KEY_MOVE_DOWN      = "f" 
          self.KEY_TURN_LEFT      = "q" 
          self.KEY_TURN_RIGHT     = "e" 
          self.KEY_LOOK_UP        = "t" 
          self.KEY_LOOK_DOWN      = "g"

     # add to lookattachment
     def add(self, child: Object3D) -> None:
          self._LookAttachment.add(child)

     # remove from lookattachment
     def remove(self, child: Object3D) -> None:
          self._LookAttachment.remove(child)

     def setMoveSpeed(self, units_per_second: float) -> None:
          self._UnitsPerSecond = units_per_second

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
          if input_object.isKeyPressed(self.KEY_MOVE_RIGHT):
               #self.translate( move_amount, 0, 0 ) 
               self.rotateY(rotate_amount, False)
          if input_object.isKeyPressed(self.KEY_MOVE_UP):
               #self.translate( 0, move_amount, 0 )
               self.rotateX(rotate_amount, False)
          if input_object.isKeyPressed(self.KEY_MOVE_DOWN):
               #self.translate( 0, -move_amount, 0 ) 
               self.rotateX(-rotate_amount, False)
          if input_object.isKeyPressed(self.KEY_TURN_RIGHT):
               self.rotateY( -rotate_amount ) 
          if input_object.isKeyPressed(self.KEY_TURN_LEFT):
               self.rotateY( rotate_amount ) 
          if input_object.isKeyPressed(self.KEY_LOOK_UP):
               self._LookAttachment.rotateX( rotate_amount ) 
          if input_object.isKeyPressed(self.KEY_LOOK_DOWN):
               self._LookAttachment.rotateX( -rotate_amount )

     def detach(self) -> None:
          if self._Parent:
               self._Parent.remove(self)

     def attach(self, target: Object3D, distance=1) -> None:
          if self._Parent:
               self.detach()
          target.add(self)
          self.setPosition([0, 0, distance])