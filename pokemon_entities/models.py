from django.db import models  # noqa F401


class Pokemon(models.Model):
    title_ru = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200, blank=True)
    title_jp = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    evolved_from = models.ForeignKey("self", null=True, on_delete=models.CASCADE)
    image = models.ImageField(null=True)

    def __str__(self):
        return self.title_ru


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
