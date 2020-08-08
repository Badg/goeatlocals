'''Temporary hard-coded bounding boxes for cities.
'''
import cachetools

# Cache city data for a max of 5 minutes
CACHE_TTL_SECONDS = 300
CITIES = {
    'oakland': {
        'left': -122.355881,
        'bottom': 37.632226,
        'right': -122.114672,
        'top': 37.885368
    }
}
CITY_CACHES = cachetools.TTLCache(maxsize=100, ttl=CACHE_TTL_SECONDS)
