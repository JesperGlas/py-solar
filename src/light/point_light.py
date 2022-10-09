from light.base_light import BaseLight

class PointLight(BaseLight):

    def __init__(self, color=[0, 0, 0], position=[0, 0, 0], attenuation=[1, 0, 0, 1]) -> None:
        super().__init__(BaseLight.POINT)
        self._LightColor = color
        self.setPosition( position )
        self._Attenuation = attenuation