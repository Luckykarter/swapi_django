from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, action
from rest_framework.views import APIView, status  # import '*' is not the best practice
from exhaust_port.models import XWing, DefenceTower, Film, Starship, Specie, Planet
import math
from rest_framework.response import Response
from exhaust_port import serializers
from APISureConnector.apisureconnector import APISureConnector
from pprint import pp

class xwinglist(APIView):
    # Does something to get xwings
    def get(self, request, **kwargs):
        x = XWing.objects.all()
        # return xwings in serialized format as well
        serializer = serializers.XwingSerializer(x, context={'request': request},
                                                 many=True)
        return Response(serializer.data)

        # data = []
        # for z in x:
        #     data.append(z.id)
        # return Response(json.dumps(data))

    def post(self, request, **kwargs):
        id = request.data.get("id")
        if not isinstance(id, int):
            return Response("Bad request")
        XWing.objects.create(**request.data)
        return Response("ok")


# no need to define it as APIView since @api_view decorator can be used
# class DefenceTowerView(APIView):
# As a pilot of XWing I can destroy the tower if it's targeting me
"""
two ways of deleting tower:
DELETE exhaust_port/defence_towers/<towerID> will destroy one tower
DELETE exhaust_port/defence_towers/xwings/my will destroy all towers aiming to my ship
"""


# helper functions that return responses
def _msg(msg):
    return {'message': msg}


def _user_have_no_xwings(user):
    return Response(
        _msg('User {} does not have any X-wings'.format(user)),
        status=status.HTTP_404_NOT_FOUND
    )


def _no_towers_targeting_xwing(xwing):
    return Response(
        _msg('No defence towers aiming to the ship {} of user {}'
             .format(xwing.name, xwing.pilot)),
        status=status.HTTP_404_NOT_FOUND
    )


def _object_does_not_exist(object, id):
    return Response(
        _msg('{} {} not found'.format(object, id)),
        status=status.HTTP_404_NOT_FOUND
    )


# List all towers, add new tower
@swagger_auto_schema(
    methods=['GET', 'POST'],
    operation_id='all_towers',
    operation_description='Retrieve All Towers',
    responses={200: openapi.Response('All Towers', serializers.DefenceTowerSerializer()),
               404: openapi.Response('Not Found')})
@api_view(['GET', 'POST'])
def all_towers(request):
    if request.method == 'POST':
        id = request.data.get("id")
        if not isinstance(id, int):
            return Response("Bad request")
        DefenceTower.objects.create(**request.data)
        return Response("ok")

    elif request.method == 'GET':
        towers = DefenceTower.objects.all()
        serializer = serializers.DefenceTowerSerializer(towers, many=True)
        return Response(serializer.data)


# list tower by ID
@swagger_auto_schema(
    methods=['GET', 'DELETE'],
    operation_id='get_tower_by_id',
    operation_description='Retrieve/Add Tower by ID',
    responses={200: openapi.Response('Tower', serializers.DefenceTowerSerializer()),
               404: openapi.Response('Not Found')})
@api_view(['GET', 'DELETE'])
def get_tower_by_id(request, **kwargs):
    pk = kwargs.get('pk')
    try:
        towers = DefenceTower.objects.get(pk=pk)
    except DefenceTower.DoesNotExist:
        return _object_does_not_exist('Tower', pk)

    if request.method == 'GET':
        serializer = serializers.DefenceTowerSerializer(towers, many=False)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        if towers.health <= 0:
            already = ' already'
        else:
            already = ''
            towers.destroy()
        return Response(_msg('Tower {}{} destroyed'.format(towers.id, already)))


# I want to be able to get all towers targeting given xwing
@swagger_auto_schema(
    methods=['GET'],
    operation_id='get_tower_by_xwing_id',
    operation_description='Retrieve Tower targeting Xwing',
    responses={200: openapi.Response('Tower', serializers.DefenceTowerSerializer()),
               404: openapi.Response('Not Found')})
@api_view(['GET'])
def get_tower_by_xwing_id(request, **kwargs):
    pk_xwing = kwargs.get('pk')
    try:
        xwing = XWing.objects.get(pk=pk_xwing)
    except XWing.DoesNotExist:
        return Response(
            _msg('X-wing with id {} not found'.format(pk_xwing)),
            status=status.HTTP_404_NOT_FOUND
        )
    towers = DefenceTower.objects.filter(target=xwing)
    if not towers:
        return _no_towers_targeting_xwing(xwing)

    serializer = serializers.DefenceTowerSerializer(towers, many=True)
    return Response(serializer.data)


# list all towers targeting MY xwing
@swagger_auto_schema(
    methods=['GET'],
    operation_id='get_tower_by_user',
    operation_description='Retrieve Tower targeting Xwing',
    responses={200: openapi.Response('Tower', serializers.DefenceTowerSerializer()),
               404: openapi.Response('Not Found')})
@api_view(['GET', 'DELETE'])
def get_tower_by_user(request):
    user = request.user
    try:
        xwing = XWing.objects.get(pilot=user.id)
    except XWing.DoesNotExist:
        return _user_have_no_xwings(user)

    towers = DefenceTower.objects.filter(target=xwing)
    if not towers:
        return _no_towers_targeting_xwing(xwing)

    if request.method == 'GET':
        serializer = serializers.DefenceTowerSerializer(towers, many=True)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        counter = 0
        for tower in towers:
            if tower.health > 0:
                tower.destroy()
                counter += 1
        return Response(_msg('Destroyed {} towers'.format(counter)))


@swagger_auto_schema(
    methods=['GET', 'POST'],
    operation_id='all_starships',
    operation_description='Retrieve All Starships',
    responses={200: openapi.Response('All starships', serializers.StarshipSerializer()),
               404: openapi.Response('Not Found')})
@api_view(['GET', 'POST'])
def all_starships(request):
    if request.method == 'GET':
        starships = Starship.objects.all()
        serializer = serializers.StarshipSerializer(starships, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        films = request.data.pop('films', None)
        starship = Starship.objects.create(**request.data)
        if films:
            starship.films.set(Film.objects.filter(id__in=films))

        return Response(_msg('Starship {} id: {} is created'.format(starship.name, starship.id)))


@swagger_auto_schema(
    methods=['GET'],
    operation_id='get_species_by_starship',
    operation_description='Get species that seen given starship',
    responses={200: openapi.Response('Tower', serializers.SpecieSerializer()),
               404: openapi.Response('Not Found')})
@api_view(['GET'])
def get_species_by_starship(request, **kwargs):
    starship_id = kwargs.get('pk')
    try:
        starship = Starship.objects.get(pk=starship_id)
    except Starship.DoesNotExist:
        return _object_does_not_exist('Starship', starship_id)

    species = Specie.objects.filter(films__in=starship.films.all())
    serializer = serializers.SpecieSerializer(species, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_species_by_producer(request, **kwargs):
    # replace underscores with spaces in producer's name
    producer = kwargs.get('name').replace('_', ' ')

    films = Film.objects.filter(producer__contains=producer)
    if not films:
        return Response(_msg('No films found for given producer'),
                        status=status.HTTP_404_NOT_FOUND)
    species = Specie.objects.filter(films__in=films)
    serializer = serializers.SpecieSerializer(species, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    methods=['GET'],
    operation_id='evacuate_planet',
    operation_description='Get number of given ships to evacuate planet')
@api_view(['GET'])
def evacuate_planet(request, **kwargs):
    planet_id = kwargs.get('planet_id')
    starship_id = kwargs.get('starship_id')
    try:
        planet = Planet.objects.get(pk=planet_id)
    except Planet.DoesNotExist:
        return _object_does_not_exist('Planet', planet_id)

    try:
        starship = Starship.objects.get(pk=starship_id)
    except Starship.DoesNotExist:
        return _object_does_not_exist('Starship', starship_id)

    if starship.passengers == 0:
        return Response(_msg('Starship {} cannot carry any passengers'.format(starship.name)))
    if planet.population == 0:
        return Response(_msg('Planet {} is uninhabited'.format(planet.name)))

    ships_needed = math.ceil(planet.population / starship.passengers)
    return Response(
        {'planet': planet.name,
         'population': planet.population,
         'evacuation_ship': starship.name,
         'passengers': starship.passengers,
         'ships_needed': ships_needed}
    )


