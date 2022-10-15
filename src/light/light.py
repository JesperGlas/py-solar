from core.object3D import Object3D

class Light(Object3D):

    def __init__(self) -> None:
        super().__init__()

        self._Ambient =     [0.2, 0.2, 0.2]
        self._Color =       [1, 1, 1]
        self._Direction =   [0, 0, 1]
        self._Position =    [0, 0, 0]