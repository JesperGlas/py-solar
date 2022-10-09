from light.base_light import BaseLight

class AmbientLight(BaseLight):

    def __init__(self, light_color=[1, 1, 1]) -> None:
        super().__init__(BaseLight.AMBIENT)
        self._LightColor = light_color