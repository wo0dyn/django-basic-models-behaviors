# -*- coding: utf-8 -*-

from datetime import datetime

from django.db import models

from .managers import CacheManager


class PublishableModel(models.Model):
    """ PublishableModel behavior """

    published_at = models.DateTimeField(blank=True, null=True, db_index=True)

    def is_published(self):
        return self.published_at is not None

    def is_not_published(self):
        return self.published_at is None

    def publish(self, *args, **kwargs):
        self.published_at = datetime.now()
        return self.save(*args, **kwargs)

    def unpublish(self, *args, **kwargs):
        self.published_at = None
        return self.save(*args, **kwargs)

    class Meta:
        abstract = True


class SoftDeletableModel(models.Model):
    """ SoftDeletableModel behavior will add deleted_at field in set the
        current timestamp instead of delete the object.
        force_delete() will actually delete the model. """

    deleted_at = models.DateTimeField(blank=True, null=True, db_index=True,
        editable=False)

    def delete(self, *args, **kwargs):
        self.deleted_at = datetime.now()
        return self.save(*args, **kwargs)

    def undelete(self, *args, **kwargs):
        self.deleted_at = None
        return self.save(*args, **kwargs)

    def has_been_deleted(self):
        return self.deleted_at is not None

    def force_delete(self, *args, **kwargs):
        return super(SoftDeletableModel, self).delete(*args, **kwargs)

    class Meta:
        abstract = True


class TimestampableModel(models.Model):
    """ TimestampableModel behavior will automatically add and set appropriate
        values to created_at and updated_at fields. """

    created_at = models.DateTimeField(auto_now_add=True, db_index=True,
        editable=False)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True,
        db_index=True, editable=False)

    class Meta:
        abstract = True
        get_latest_by = "updated_at"
        ordering = ('-updated_at', '-created_at',)


class CacheableModel(models.Model):
    """ CacheableModel added a CacheManager for get() and get_or_create()
        methods to load data only once from the database """

    cache = CacheManager()
    objects = models.Manager()

    class Meta:
        abstract = True
