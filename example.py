from src.core import *

def main():
    API = NOWCAST(latitude=70.3105, longitude=31.0241)

    print("Pressure:", API.get_pressure())
    print("Wind direction: ", API.get_wind_direction())
    print("Wind speed: ", API.get_wind_speed())
    print("Precipitation rate: ", API.get_precipitation_rate())

if __name__ == '__main__':
    main()