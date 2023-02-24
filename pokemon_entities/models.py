from django.db import models  # noqa F401


class Pokemon(models.Model):
    text = models.CharField(max_length=200)
    image = models.ImageField(null=True)

    def __str__(self):
        return self.text


class PokemonEntity(models.Model):
    lat = models.FloatField()
    lon = models.FloatField()

    def __str__(self):
        return f'lat - {self.lat} : lon - {self.lon}'
