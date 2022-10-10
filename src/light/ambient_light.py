from light.light import Light

class AmbientLight(Light):

    def __init__(self, color=[1, 1, 1]) -> None:
        super().__init__(Light.AMBIENT)
        self._LightColor = color