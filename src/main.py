from service.service_open_solar import OrbitalInformation

TITLE: str = "Solarpy"
VERSION: str = "1.0.0"
AUTHOR: str = "Jesper Glas"

def main():
    print(f'Running {TITLE} version {VERSION}')

    oi: OrbitalInformation = OrbitalInformation()
    
    star = oi.getStar()
    planets = oi.getPlanets()
    moons = oi.getMoons()
            
if __name__ == '__main__':
    main()