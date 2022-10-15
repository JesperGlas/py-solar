import numpy as np
from typing import Dict, List
from core.matrix import Matrix

class Object3D(object):

    def __init__(self) -> None:
        self._Transform = Matrix.makeIdentity()
        self._Parent: Object3D = None
        self._Children: List[Object3D] = []

    def _type(self):
        return self.__class__.__name__

    def add(self, child: object) -> None:
        self._Children.append(child)
        child._Parent = self

    def remove(self, child: object) -> None:
        self._Children.remove(child)
        child._Parent = None

    def getRoot(self) -> object:
        current = self._Parent
        while current._Parent != None:
            current = current._Parent
        return current

    def getWorldMatrix(self) -> Matrix:
        if self._Parent == None:
            return self._Transform
        else:
            return self._Parent.getWorldMatrix() @ self._Transform

    def getDescendantList(self) -> List[object]:
        descendants: List[Object3D] = []
        nodes_to_process: List[Object3D] = [self]
        while len(nodes_to_process) > 0:
            node = nodes_to_process.pop(0)
            descendants.append(node)
            nodes_to_process = node._Children + nodes_to_process
        
        return descendants

    def applyMatrix(self, matrix: Matrix, local_coord: bool=True) -> None:
        if local_coord:
            self._Transform = self._Transform @ matrix
        else:
            self._Transform = matrix @ self._Transform

    def translate(self, x, y, z, local_coord: bool=True) -> None:
        m = Matrix.makeTranslation(x, y, z)
        self.applyMatrix(m, local_coord)

    def rotateX(self, angle, local_coord: bool=True) -> None:
        m = Matrix.makeRotationX(angle)
        self.applyMatrix(m, local_coord)

    def rotateY(self, angle, local_coord: bool=True) -> None:
        m = Matrix.makeRotationY(angle)
        self.applyMatrix(m, local_coord)

    def rotateZ(self, angle, local_coord: bool=True) -> None:
        m = Matrix.makeRotationZ(angle)
        self.applyMatrix(m, local_coord)

    def scale(self, scale, local_coord: bool=True) -> None:
        m = Matrix.makeScale(scale, local_coord)

    def getPosition(self):
        return [
            self._Transform.item((0, 3)),
            self._Transform.item((1, 3)),
            self._Transform.item((2, 3))
        ]

    def getWorldPosition(self):
        world_transform: Matrix = self.getWorldMatrix()
        return [
            world_transform.item((0, 3)),
            world_transform.item((1, 3)),
            world_transform.item((2, 3))
        ]

    def setPosition(self, position: List):
        self._Transform.itemset((0, 3), position[0])
        self._Transform.itemset((1, 3), position[1])
        self._Transform.itemset((2, 3), position[2])

    def getDirectionTowards(self, target_position):
        return Matrix.makeLookAt(self.getWorldPosition(), target_position)

    def getDirectionTowardsObject(self, target: object):
        return self.getDirectionTowards(target.getWorldPosition())

    def lookAt(self, target_position):
        self._Transform = Matrix.makeLookAt(
            self.getWorldPosition(),
            target_position )

    def lookAtObject(self, target: object, local_coord: bool=True) -> None:
        if local_coord:
            self.lookAt(target.getPosition())
        else:
            self.lookAt(target.getWorldPosition())

    def getOrientationMatrix(self):
        return np.array([
            self._Transform[0][0:3],
            self._Transform[1][0:3],
            self._Transform[2][0:3] ])

    def getDirection(self):
        forward = np.array( [0, 0, -1] )
        return list( self.getOrientationMatrix() @ forward )

    def setDirection(self, direction) -> None:
        position = self.getPosition()
        target_position = [
            position[0] + direction[0],
            position[1] + direction[1],
            position[2] + direction[2] ]
        self.lookAt( target_position )

    def printNodeTree(self, depth: int=0) -> None:
        print("- " + "\t"*depth + f"{self._type()}")
        for child in self._Children:
            child.printNodeTree(depth+1)