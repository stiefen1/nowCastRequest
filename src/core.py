import requests, time
from src.utils import *
from geopy.geocoders import Nominatim

HEADERS = {
    "User-Agent": "randomUser@NowCastRequest"  # Replace with your app name and contact information
}

# more info here: https://api.met.no/doc/ForecastJSON
NOWCAST_BASE_URL = "https://api.met.no/weatherapi/nowcast/2.0/complete?lat={}&lon={}"

# More info here: https://api.met.no/weatherapi/nowcast/2.0/documentation
class NOWCAST:
    def __init__(self, url:str=None, latitude:float=None, longitude:float=None, city:str=None):
        
        if url is not None:
            self._init_from_url(url)
            
        elif latitude is not None and longitude is not None:
            self._init_from_lat_long(latitude, longitude)

        elif city is not None:
            self._init_from_city(city)
        else:
            self._init_to_none()

    def _init_from_url(self, url:str) -> None:
        self._url:str = url if isURLValid(url) else None
        latLong:tuple = getLatLongFromURL(url)[0]
        self._latitude:float = latLong[0]
        self._longitude:float = latLong[1]

    def _init_from_lat_long(self, latitude:float, longitude:float) -> None:
        self._latitude:float = latitude
        self._longitude:float = longitude
        self._url:str = getURLFromLatLong(self._latitude, self._longitude, NOWCAST_BASE_URL)

    def _init_from_city(self, city:str) -> None:
        geolocator = Nominatim(user_agent="MyApp")
        location = geolocator.geocode(city)
        self._latitude = location.latitude
        self._longitude = location.longitude
        self._url:str = getURLFromLatLong(self._latitude, self._longitude, NOWCAST_BASE_URL)

    def _init_to_none(self) -> None:
        self._url:str = None
        self._latitude:float = None
        self._longitude:float = None
        
    def get(self, maxRequestCount:int = 5, timeInterval:float = 0.5) -> requests.Response:
        requestCount:int = 0
        while requestCount < maxRequestCount:
            try: 
                response = requests.get(self._url, headers=HEADERS)
                return response
            except requests.exceptions.RequestException as e:
                requestCount += 1
                print(f"Attempt {requestCount}/{maxRequestCount} failed in get : ", e)
                time.sleep(timeInterval)

        return None
    
    def get_as_json(self, maxRequestCount:int = 5, timeInterval:float = 0.5) -> dict:
        response:requests.Response = self.get(maxRequestCount=maxRequestCount, timeInterval=timeInterval)
        if response is not None:
            return response.json()
        else:
            return None
    
    def get_pressure(self) -> list[tuple]:
        return self.get_data('air_pressure_at_sea_level')

    def get_air_temperature(self) -> list[tuple]:
        return self.get_data('air_temperature') 

    def get_precipitation(self) -> list[tuple]:
        return self.get_data('precipitation_amount')
    
    def get_precipitation_rate(self) -> list[tuple]:
        return self.get_data('precipitation_rate')

    def get_wind(self) -> list[tuple]:
        pass

    def get_wind_speed(self) -> list[tuple]:
        return self.get_data('wind_speed')

    def get_wind_direction(self) -> list[tuple]:
        return self.get_data('wind_from_direction')

    def get_data(self, name:str) -> list[tuple]:
        json = self.get_as_json()
        data = []
        if json is None:
            return []
        for i, timeserie_i in enumerate(json["properties"]["timeseries"]):
            try:
                data_i = timeserie_i["data"]["instant"]["details"][name]
                timestamp_i = timeserie_i["time"]
                data.append((timestamp_i, data_i))
            except:
                pass

        return data


    def _update_url(self) -> None:
        self._url = getURLFromLatLong(self._latitude, self._longitude, NOWCAST_BASE_URL)

    def _update_lat_long(self) -> None:
        self._latitude = getLatLongFromURL(self._url)[0]
        self._longitude = getLatLongFromURL(self._url)[1]
    
    @property
    def url(self) -> str:
        if self._url is None and isLatitudeValid(self._latitude) and isLongitudeValid(self._longitude):
            self._url = getURLFromLatLong(self._latitude, self._longitude, NOWCAST_BASE_URL)
        return self._url
    @property
    def latitude(self) -> float:
        if self._latitude is None and isURLValid(self._url):
            self._latitude = getLatLongFromURL(self._url)[0]
        return self._latitude
    @property
    def longitude(self) -> float:
        if self._longitude is None and isURLValid(self._url):
            self._longitude = getLatLongFromURL(self._url)[1]
        return self._longitude

    @url.setter
    def url(self, url:str) -> None:
        self._set_url(url)

    @latitude.setter
    def latitude(self, latitude:float) -> None:
        self._set_latitude(latitude)

    @longitude.setter
    def longitude(self, longitude:float) -> None:
        self._set_longitude(longitude)

    def _set_url(self, url:str) -> None:
        if(isURLValid(url)):
            self._url = url
            self._update_lat_long()

    def _set_latitude(self, latitude:float) -> None:
        if(isLatitudeValid(latitude)):
            self._latitude = latitude
            self._update_url()

    def _set_longitude(self, longitude:float) -> None:
        if(isLongitudeValid(longitude)):
            self._longitude = longitude
            self._update_url()
