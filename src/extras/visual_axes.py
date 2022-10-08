from core.mesh import Mesh
from geometry.geometry import Geometry
from material.line_material import LineMaterial

class VisualAxes(Mesh):

    def __init__(self, axis_length=1, axis_width=4, axis_colors=[
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ]):

        # create position data
        geometry = Geometry()
        # position data
        position_data = [
            [0, 0, 0], [axis_length, 0, 0],
            [0, 0, 0], [0, axis_length, 0],
            [0, 0, 0], [0, 0, axis_length]
        ]
        # color data
        color_data = [
            axis_colors[0], axis_colors[0],
            axis_colors[1], axis_colors[1],
            axis_colors[2], axis_colors[2]
        ]

        geometry.addAttribute("vec3", "a_position", position_data)
        geometry.addAttribute("vec3", "a_color", color_data)
        geometry.countVertecies()

        material = LineMaterial({
            "u_useVertexColors":    True,
            "lineWidth":            axis_width,
            "lineType":             "segments"
        })

        # init the mesh        
        super().__init__(geometry, material)