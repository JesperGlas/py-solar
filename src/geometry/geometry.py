import numpy as np
from typing import Dict
from core.attribute import Attribute
from core.matrix import Matrix

class Geometry(object):

    def __init__(self) -> None:
        
        self._Attributes: Dict[str, Attribute] = {}
        self._VertexCount: int = None

    def addAttribute(self, data_type: str, variable_name: str, data) -> None:
        self._Attributes[variable_name] = Attribute(data_type, data)

    def countVertecies(self) -> None:
        attrib: Attribute = list(self._Attributes.values())[0]
        self._VertexCount = len(attrib._Data)

    def applyMatrix(self, matrix: Matrix) -> None:
        rotation_matrix = np.array([
            matrix[0][0:3],
            matrix[1][0:3],
            matrix[2][0:3] ])

        # change normals if matrix is applied (Only affected by rotations)
        old_vert_norm_data = self._Attributes["a_vNormal"]._Data
        new_vert_norm_data = []
        for old_norm in old_vert_norm_data:
            new_normal = old_norm.copy()
            new_normal = rotation_matrix @ new_normal
            new_vert_norm_data.append(new_normal)
        # update attribute
        self._Attributes["a_vNormal"]._Data = new_vert_norm_data

        old_face_norm_data = self._Attributes["a_fNormal"]._Data
        new_face_norm_data = []
        for old_norm in old_face_norm_data:
            new_normal = old_norm.copy()
            new_normal = rotation_matrix @ new_normal
            new_face_norm_data.append(new_normal)
        # update attribute
        self._Attributes["a_fNormal"]._Data = new_face_norm_data

        