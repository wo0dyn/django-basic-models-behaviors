from django.db import models

from basic_models_behaviors.models import PublishableModel, SoftDeletableModel, TimestampableModel, CacheableModel, SlugableModel


class PublishableMock(PublishableModel):
    pass


class SoftDeletableMock(SoftDeletableModel):
    pass


class TimestampableMock(TimestampableModel):
    pass


class CacheableMock(CacheableModel):
    name = models.CharField(max_length=150, null=True, blank=True)


class SlugableMock(SlugableModel):
    label = models.CharField(max_length=255)
