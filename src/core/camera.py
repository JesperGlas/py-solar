from core.object3D import Object3D
from core.matrix import Matrix
from numpy.linalg import inv

class Camera(Object3D):

    def __init__(self, angle_of_view=60, aspect_ratio=1, near=0.1, far=1000) -> None:
        super().__init__()
        
        self._ProjectionMatrix = Matrix.makePerspective(angle_of_view, aspect_ratio, near, far)
        self._ViewMatrix = Matrix.makeIdentity()

    def setPerspective(self, angle_of_view=60, aspect_ratio=1, near=0.1, far=1000) -> None:
        self._ProjectionMatrix = Matrix.makePerspective(angle_of_view, aspect_ratio, near, far)

    def setOrthographic(self, left=-1, right=1, bottom=-1, top=1, near=-1, far=1) -> None:
        self._ProjectionMatrix = Matrix.makeOrthographic(left, right, bottom, top, near, far)

    def updateViewMatrix(self) -> None:
        self._ViewMatrix = inv(self.getWorldMatrix())