from django.apps import AppConfig
import sys

class ExhaustPortConfig(AppConfig):
    name = "exhaust_port"
    # load all the data from SWAPI once when server started
    def ready(self):
        if 'runserver' in sys.argv:
            # import is relevant only when server is ready
            from exhaust_port.loaddata import load_data_from_swapi
            load_data_from_swapi()
