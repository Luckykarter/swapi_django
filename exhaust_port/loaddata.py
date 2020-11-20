import requests
from exhaust_port.models import Film, Starship, Planet, Specie

def load_data_from_swapi():
    # to avoid loading the data from SWAPI every time on application loading
    # (to save time during tests)
    # the flag might be set to False - only local data from DB will be used
    RELOAD_DATA = False

    if RELOAD_DATA:
        URL = "https://swapi.dev/api/"
        print('Loading data from:', URL)

        urls = [URL + category for category in [
            'films/', 'starships/', 'planets/', 'species/'
        ]]
        for i, Class in enumerate([Film, Starship, Planet, Specie]):
            res = requests.get(urls[i])
            results = res.json().get('results')
            if not results:
                raise ConnectionError('No data received from SWAPI\nURL: {}'.format(urls[i]))

            for result in results:
                obj = Class()
                obj.load(result)
