import pytest
from .test_models import defence_tower
from exhaust_port.models import DefenceTower
from exhaust_port.loaddata import load_data_from_swapi
from math import ceil

@pytest.fixture
def types():
    return ['xwings', 'defence_towers']

# replaced with more generic test

# @pytest.mark.django_db
# class TestGetXWings:
#     def test_get(self, client):
#         response = client.get("/exhaust_port/xwings/")
#         assert response.status_code == 200

@pytest.mark.django_db
class TestGetItems:
    def test_get(self, client, types):
        for type in types:
            response = client.get('/exhaust_port/{}/'.format(type))
            assert response.status_code == 200


@pytest.fixture
def requests(admin_user):
    return {
        'xwings': {
            'pilot': admin_user,
            'cost': 'fewfew',
            'name': 'test_name',
            '_coordinates': '20202'
        },
        'defence_towers': {
            'id': 1,
            'sector': 1,
            'health': 100,
            'cost': 123456,
        }
    }

@pytest.mark.django_db
class TestPostItem:
    def test_post(self, client, types, requests):
        for type in types:
            request = requests[type]
            response = client.post('/exhaust_port/{}/'.format(type), request)
            assert response.status_code == 200

@pytest.mark.django_db
class TestGetDefenceTower:
    def test_get(self, client, defence_tower):
        tower = defence_tower
        tower.save()
        response = client.get('/exhaust_port/defence_towers/1')
        assert response.status_code == 200
    def test_delete(self, client, defence_tower):
        # first create a tower
        tower = defence_tower
        tower.save()

        # then try to destroy it
        response = client.delete('/exhaust_port/defence_towers/1')
        assert response.status_code == 200
        tower = DefenceTower.objects.get(id=1)
        assert tower.health == 0

@pytest.mark.django_db
class TestGetSpecies:
    def test_by_ship(self, client):
        load_data_from_swapi()
        response = client.get('/exhaust_port/species/starships/9')
        assert response.status_code == 200
    def test_by_producer(self, client):
        load_data_from_swapi()
        response = client.get('/exhaust_port/species/starships/producers/George_Lucas')
        assert response.status_code == 200

@pytest.mark.django_db
class TestEvacuation:
    # test calculation of ships needed for evacuation
    def test_number_of_ships(self, client):
        load_data_from_swapi()
        response = client.get('/exhaust_port/evacuate_planet/9/starships/2')
        assert response.status_code == 200

        results = response.json()
        population = results.get('population')
        passengers = results.get('passengers')
        ships_needed = results.get('ships_needed')
        assert ceil(population/passengers) == ships_needed



