from light.base_light import BaseLight

class DirectionalLight(BaseLight):

    def __init__(self, color=[1, 1, 1], direction=[0, -1, 0]) -> None:
        super().__init__(BaseLight.DIRECTIONAL)
        self._LightColor = color
        self.setDirection(direction)