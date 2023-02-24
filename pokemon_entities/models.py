from django.db import models  # noqa F401


class Pokemon(models.Model):
    text = models.CharField(max_length=200)
