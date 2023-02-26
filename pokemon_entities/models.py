from django.db import models  # noqa F401


class Pokemon(models.Model):
    title_ru = models.CharField(max_length=200, verbose_name='Имя покемона на русском')
    title_en = models.CharField(max_length=200, blank=True, verbose_name='Имя покемона на английском')
    title_jp = models.CharField(max_length=200, blank=True, verbose_name='Имя покемона на японском')
    description = models.TextField(blank=True, verbose_name='Описание покемона')
    evolved_from = models.ForeignKey("self", null=True, on_delete=models.CASCADE,
                                     related_name="pokemons", related_query_name="pokemon_evolution",
                                     verbose_name='Из кого эволюционировал покемон')
    image = models.ImageField(null=True, verbose_name='Картинка покемона')

    def __str__(self):
        return self.title_ru


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, verbose_name='Покемон')
    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')
    appeared_at = models.DateTimeField(verbose_name='Время появления')
    disappear_at = models.DateTimeField(verbose_name='Время исчезновения')
    level = models.IntegerField(default=1, verbose_name='Уровень покемона')
    health = models.IntegerField(default=100, verbose_name='Здоровье покемона')
    strength = models.IntegerField(default=10, verbose_name='Сила покемона')
    defence = models.IntegerField(default=5, verbose_name='Защита покемона')
    stamina = models.IntegerField(default=100, verbose_name='Стамина (выносливость) покемона')

    def __str__(self):
        return f'lat - {self.lat} : lon - {self.lon}'
