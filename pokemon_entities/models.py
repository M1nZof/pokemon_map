from django.db import models  # noqa F401


class Pokemon(models.Model):
    text = models.CharField(max_length=200)
    image = models.ImageField(null=True)

    def __str__(self):
        return self.text


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    lat = models.FloatField()
    lon = models.FloatField()
    appeared_at = models.DateTimeField()
    disappear_at = models.DateTimeField()
    level = models.IntegerField(default=1)
    health = models.IntegerField(default=100)
    strength = models.IntegerField(default=10)
    defence = models.IntegerField(default=5)
    stamina = models.IntegerField(default=100)

    def __str__(self):
        return f'lat - {self.lat} : lon - {self.lon}'
