class StellarUtils(object):

    WORLD_RADIUS: float =   1e4         # units
    ACTUAL_RADIUS: float =  4.49506e9   # km
    SCALE: float =          WORLD_RADIUS / ACTUAL_RADIUS # fractal

    @classmethod
    def unitToKm(cls, units: float) -> float:
        return units / cls.SCALE

    @classmethod
    def kmToUnits(cls, km: float) -> float:
        return km * cls.SCALE