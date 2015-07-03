from django.db import models

from basic_models_behaviors import models as models_behaviors


class PublishableMock(models_behaviors.PublishableModel):
    pass


class SoftDeletableMock(models_behaviors.SoftDeletableModel):
    pass


class TimestampableMock(models_behaviors.TimestampableModel):
    pass


class CacheableMock(models_behaviors.CacheableModel):
    name = models.CharField(max_length=150, null=True, blank=True)


class SlugableMock(models_behaviors.SlugableModel):
    label = models.CharField(max_length=255)
