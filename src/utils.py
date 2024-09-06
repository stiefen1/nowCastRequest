LATTITUDE_RANGE = (-90., 90.)
LONGITUDE_RANGE = (-180., 180.)

def isLatitudeValid(lat:float) -> bool:
    return isFloatInRange(lat, *LATTITUDE_RANGE)

def isLongitudeValid(long:float) -> bool:
    return isFloatInRange(long, *LONGITUDE_RANGE)

def isFloatInRange(value:float, minValue:float, maxValue:float) -> bool:
    if value is None:
        return False
    if value < minValue or value > maxValue:
        return False
    return True

def isURLValid(url:str) -> bool:
    lat, long = getLatLongFromURL(url)
    conditions:dict = {
        'startCondition':url.startswith('http://') or url.startswith('https://'),
        'containsValidDomain':'api.met.com' in url,
        'containsValidLongitude': isLongitudeValid(long),
        'containsValidLatitude': isLatitudeValid(lat)
    }

    return sum(conditions.values()) == len(conditions)

def getURLFromLatLong(latitude:float, longitude:float, BASE_URL:str) -> str:
    try:
        return BASE_URL.format(latitude, longitude)
    except Exception as e:
        print("Error in getURLFromLatLong: ", e)
        return None
    
def getLatLongFromURL(url:str) -> tuple:
    if not isURLValid(url):
        return None, None
    try:
        lat:float = float(url.split('lat=')[-1].split('&')[0])
        long:float = float(url.split('lon=')[-1])
        if not isLatitudeValid(lat) or not isLongitudeValid(long):
            return None, None
        else:
            return lat, long
    except Exception as e:
        print("Error in getLatLongFromURL: ", e)
        return None