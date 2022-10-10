from light.light import Light

class PointLight(Light):

    def __init__(self, color=[1, 1, 1], position=[0, 0, 0], attenuation=[1, 0, 0.1]) -> None:
        super().__init__(Light.POINT)
        self._LightColor = color
        self.setPosition( position )
        self._Attenuation = attenuation