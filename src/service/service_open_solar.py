import os
import requests
import json
from typing import Dict, List


BODIES_URL: str = "https://api.le-systeme-solaire.net/rest/bodies/"

class OrbitalInformation:
    def __init__(self):
        self.bodies: Dict[str, Dict]= self.loadPlanets()

    def loadPlanets(self) -> Dict[str, Dict]:
        parameters = {'data': 'id,name,bodyType,aroundPlanet'}
        res = requests.get(BODIES_URL, params=parameters)
        
        res_code: int = res.status_code
        print(f'Response status: {res_code}')
        data = res.text
        
        json_data = json.loads(data)
        res: Dict[str, Dict] = {}
        for entry in json_data['bodies']:
            res[entry['name']] = entry

        return res

    def getPlanets(self) -> Dict[str, Dict]:
        res: Dict[str, Dict] = {}
        for key, data in self.bodies.items():
            if data['bodyType'] == "Planet":
                res[key] = data
        return res
    
    def getStar(self) -> Dict:
        for data in self.bodies.values():
            if data['bodyType'] == "Star":
                return data
    
    def getMoons(self) -> Dict[str, Dict]:
        res: Dict[str, Dict] = {}
        for key, data in self.bodies.items():
            if data['bodyType'] == "Moon":
                res[key] = data
            return res