from django.db import models  # noqa F401


class Pokemon(models.Model):
    title_ru = models.CharField(max_length=200, verbose_name='Имя покемона на русском')
    title_en = models.CharField(max_length=200, verbose_name='Имя покемона на английском', null=True, blank=True)
    title_jp = models.CharField(max_length=200, verbose_name='Имя покемона на японском', null=True, blank=True)
    description = models.TextField(blank=True, verbose_name='Описание покемона')
    evolved_from = models.ForeignKey("self", null=True, on_delete=models.CASCADE,
                                     related_name="pokemon_evolutions", related_query_name="pokemon_evolution",
                                     verbose_name='Из кого эволюционировал покемон')
    image = models.ImageField(null=True, verbose_name='Картинка покемона')

    def __str__(self):
        return self.title_ru


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, verbose_name='Покемон')
    lat = models.FloatField(verbose_name='Широта', null=True)
    lon = models.FloatField(verbose_name='Долгота', null=True)
    appeared_at = models.DateTimeField(verbose_name='Время появления', null=True)
    disappear_at = models.DateTimeField(verbose_name='Время исчезновения', null=True)
    level = models.IntegerField(verbose_name='Уровень покемона', null=True, blank=True)
    health = models.IntegerField(verbose_name='Здоровье покемона', null=True, blank=True)
    strength = models.IntegerField(verbose_name='Сила покемона', null=True, blank=True)
    defence = models.IntegerField(verbose_name='Защита покемона', null=True, blank=True)
    stamina = models.IntegerField(verbose_name='Стамина (выносливость) покемона', null=True, blank=True)

    def __str__(self):
        return f'lat - {self.lat} : lon - {self.lon}'
