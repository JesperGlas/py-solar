from OpenGL.GL import *
from core.object3D import Object3D
from core.attribute import Attribute
from material.material import Material
from geometry.geometry import Geometry

class Mesh(Object3D):

    def __init__(self, geometry: Geometry, material: Material) -> None:
        super().__init__()

        self._Geometry = geometry
        self._Material = material
        self._Visible = True

        self._VaoRef = glGenVertexArrays(1)
        glBindVertexArray(self._VaoRef)

        attribute_object: Attribute
        for variable_name, attribute_object in geometry._Attributes.items():
            attribute_object.associateVariable(variable_name, material._ProgramRef)
        
        # unbind vao
        glBindVertexArray(0)