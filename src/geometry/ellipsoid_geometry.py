from geometry.parametric_geometry import ParametricGeometry
from math import sin, cos, pi

class EllipsoidGeometry(ParametricGeometry):

    def __init__(self, width=1, height=1, depth=1, radius_seg=32, height_seg=16):

        def S(u, v):
            return [
                width/2 * sin(u) * cos(v),
                height/2 * sin(v),
                depth/2 * cos(u) * cos(v)
            ]
        
        super().__init__(0, 2*pi, radius_seg, -pi/2, pi/2, height_seg, S)