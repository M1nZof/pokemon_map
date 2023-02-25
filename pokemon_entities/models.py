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

    def __str__(self):
        return f'lat - {self.lat} : lon - {self.lon}'
