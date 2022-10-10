from core.object3D import Object3D

class Light(Object3D):

    AMBIENT = 1
    DIRECTIONAL = 2
    POINT = 3
    def __init__(self, light_type=0) -> None:
        super().__init__()

        self._LightType     = light_type
        self._LightColor    = [1, 1, 1]
        self._Attenuation   = [1, 0, 0]