from turtle import position
from geometry.geometry import Geometry

class RectangleGeometry(Geometry):

    def __init__(self, width=1, height=1) -> None:
        super().__init__()

        p0 = [-width/2, -height/2, 0]
        p1 = [ width/2, -height/2, 0]
        p2 = [-width/2,  height/2, 0]
        p3 = [ width/2,  height/2, 0]

        c0, c1, c2, c3 = [1, 1, 1], [1, 0, 0], [0, 1, 0], [0, 0, 1]

        position_data = [
            p0, p1, p3,
            p0, p3, p2 ]
        color_data = [
            c0, c1, c3,
            c0, c3, c2 ]

        self.addAttribute("vec3", "a_position", position_data)
        self.addAttribute("vec3", "a_color", color_data)
        self.countVertecies()

        # texture coordinates
        t0, t1, t2, t3 = [0, 0], [1, 0], [0, 1], [1, 1]
        texture_data = [t0, t1, t3, t0, t3, t2]
        self.addAttribute("vec2", "a_texCoords", texture_data)

        # normals
        normal_vector = [0 ,0, 1]
        normal_data = [normal_vector] * 6
        self.addAttribute("vec3", "a_vNormal", normal_data)
        self.addAttribute("vec3", "a_fNormal", normal_data)