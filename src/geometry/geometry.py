from typing import Dict
from core.attribute import Attribute

class Geometry(object):

    def __init__(self) -> None:
        
        self._Attributes: Dict[str, Attribute] = {}

        self._VertexCount: int = None

    def addAttribute(self, data_type: str, variable_name: str, data) -> None:
        self._Attributes[variable_name] = Attribute(data_type, data)

    def countVertecies(self) -> None:
        attrib: Attribute = list(self._Attributes.values())[0]
        self._VertexCount = len(attrib._Data)