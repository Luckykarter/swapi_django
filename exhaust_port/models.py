from django.contrib.auth.models import User
from django.db import models

'''
Models to get data from SWAPI
each model has method load() which extracts necessary
fields from dictionary (JSON) received from SWAPI and
saves one object in DB

'''


class Film(models.Model):
    title = models.CharField(max_length=200)
    producer = models.CharField(max_length=200)
    url = models.URLField(null=True)
    episode_id = models.IntegerField(default=0)

    def load(self, film: dict) -> None:
        self.id = get_id_from_url(film.get('url'))
        self.producer = film.get('producer', '?')
        self.episode_id = film.get('episode_id')
        self.title = film.get('title', '?')
        self.url = film.get('url', '?')
        self.save()

    def __str__(self):
        return 'Episode {}: {}'.format(self.id, self.title)


class Starship(models.Model):
    name = models.CharField(max_length=200, default='Unknown Starship')
    passengers = models.IntegerField()
    films = models.ManyToManyField(Film)

    CATEGORY = [
        ('F', 'Food'),
        ('L', 'Living Item'),
    ]

    category = models.CharField(
        verbose_name='Category',
        max_length=1,
        choices=CATEGORY,
        default='F'
    )

    def load(self, starship: dict):
        self.id = get_id_from_url(starship.get('url'))
        self.name = starship.get('name', '?')
        self.passengers = get_int_value(starship.get('passengers'))
        self.save()
        self.films.set(Film.objects.filter(id__in=[get_id_from_url(url)
                                                   for url in starship.get('films')]))

    def __str__(self):
        return self.name


class Specie(models.Model):
    name = models.CharField(max_length=1000, default='Unknown Specie')
    films = models.ManyToManyField(Film)

    def load(self, specie: dict) -> None:
        self.id = get_id_from_url(specie.get('url'))
        self.name = specie.get('name', '?')
        self.save()
        self.films.set(Film.objects.filter(id__in=[get_id_from_url(url)
                                                   for url in specie.get('films')]))

    def __str__(self):
        return self.name


class Planet(models.Model):
    name = models.CharField(max_length=200, default='Unknown Planet')
    population = models.IntegerField()

    def load(self, planet: dict) -> None:
        self.id = get_id_from_url(planet.get('url'))
        self.name = planet.get('name', '?')
        self.population = get_int_value(planet.get('population'))
        self.save()

    def __str__(self):
        return 'planets'


class XWing(models.Model):
    pilot = models.OneToOneField(User, on_delete=models.CASCADE)
    health = models.IntegerField(default=100, help_text="between 0 and 100")
    cost = models.FloatField(help_text="Cost in US $")
    name = models.CharField(max_length=12000)
    _coordinates = models.CharField(max_length=10000)

    def destroy(self):
        while self.health > 0:
            self.health -= 1
            self.save()

    def set_name(self, newName):
        self.name = newName

    def get_name(self):
        return self.name

    def is_destroyed(self, damage):
        return self.health - damage == 0

    def set_coordinates(self, x, y, z):
        coordinates = f"{x}0{y}0{z}"
        self._coordinates = coordinates

    def get_coordinates(self):
        x, y, z = self._coordinates.split("0")
        return int(x), int(y), int(z)

    def __str__(self):
        return self.name


class DefenceTower(models.Model):
    sector = models.CharField(
        max_length=1000, choices=(("a1", 1), ("a2", 2), ("b1", 3), ("b2", 4))
    )
    health = models.IntegerField(default=100)
    cost = models.FloatField(help_text="Cost in US $")
    _coordinates = models.CharField(max_length=10000)
    target = models.ForeignKey(
        "exhaust_port.XWing", on_delete=models.SET_NULL, null=True
    )

    def is_destroyed(self, damage):
        return self.health - damage == 0

    def destroy(self):
        while self.health > 0:
            self.health -= 1
            self.save()

    def set_coordinates(self, x, y, z):
        coordinates = f"{x}0{y}0{z}"
        self._coordinates = coordinates

    def get_coordinates(self):
        x, y, z = self._coordinates.split("0")
        return int(x), int(y), int(z)

# convert string to an integer (zero when conversion failed)
def get_int_value(value: str) -> int:
    try:
        return int(value)
    except ValueError:
        return 0


# use SWAPI's ids as primary keys in our DB - extract from URL
def get_id_from_url(url: str):
    id = get_int_value(list(filter(None, url.split('/')))[-1])
    if id > 0:
        return id
    else:
        # when nothing returned - id will be assigned as next key available
        return None
