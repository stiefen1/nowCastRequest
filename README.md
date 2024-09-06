# NowCastRequest

A very simple wrapper to get weather data from api.met.no (Nowcast).

```
from src.core import *

def main():
    API = NOWCAST(latitude=70.3105, longitude=31.0241)

    # Or directly instantiate it with the city you're interested in:  API = NOWCAST(city="Trondheim")

    print("Pressure:", API.get_pressure())
    print("Wind direction: ", API.get_wind_direction())
    print("Wind speed: ", API.get_wind_speed())
    print("Precipitation rate: ", API.get_precipitation_rate())

if __name__ == '__main__':
    main()
```

# Requirements
This wrapper only requires requests and geopy packages:

```pip install requests geopy```