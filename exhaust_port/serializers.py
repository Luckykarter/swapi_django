from rest_framework import serializers
from .models import DefenceTower, XWing, Specie, Starship, Film


# add information of X-wing as well into defence tower serializer
class XwingSerializer(serializers.ModelSerializer):
    pilot = serializers.StringRelatedField(many=False)

    class Meta:
        model = XWing
        fields = ['id', 'name', 'pilot']


# representation for defence towers
class DefenceTowerSerializer(serializers.ModelSerializer):
    target = XwingSerializer()

    class Meta:
        model = DefenceTower
        fields = '__all__'


class FilmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = '__all__'


class SpecieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specie
        fields = '__all__'


class StarshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Starship
        fields = '__all__'