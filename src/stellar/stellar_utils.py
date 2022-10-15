
class StellarUtils(object):

    KM_RADIUS = 5.90911589e9
    UNIT_RADIUS = 1e4

    EARTH_TO_SUN = 1.4917e8
    MOON_TO_EARTH = 3.844e5

    @classmethod
    def km2Unit(cls, km: float) -> float:
        return km / (cls.KM_RADIUS/cls.UNIT_RADIUS)

    @classmethod
    def unit2Km(cls, units: float) -> float:
        return units * (cls.KM_RADIUS/cls.UNIT_RADIUS)

    @classmethod
    def getSunRadius(cls) -> float:
        return cls.km2Unit(6.69e5)

    @classmethod
    def getEarthRadius(cls) -> float:
        return cls.km2Unit(6.37e3)

    @classmethod
    def getEarthSunDistance(cls) -> float:
        return cls.km2Unit(cls.EARTH_TO_SUN)

    @classmethod
    def getMoonRadius(cls) -> float:
        return cls.km2Unit(1.73e3)
    
    @classmethod
    def getMoonEarthDistance(cls) -> float:
        return cls.km2Unit(cls.MOON_TO_EARTH)