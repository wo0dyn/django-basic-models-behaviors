# -*- coding: utf-8 -*-

from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.core.cache import cache
from django.template.defaultfilters import slugify

from .managers import CacheManager, get_key_for_instance


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
    """ CacheableModel added a CacheManager for query
        methods to load data only once from the database """

    objects = CacheManager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        super(CacheableModel, self).save(*args, **kwargs)
        cache.set(get_key_for_instance(self), self, 60 * 60 * 24)

    def delete(self):
        cache.delete(get_key_for_instance(self))
        super(CacheableModel, self).delete()


class SlugableModel(models.Model):
    """ SlugableModel generate unique model slugs """

    slug = models.SlugField(editable=False)

    class Meta:
        abstract = True

    def _make_slug(self):
        return slugify('{0}'.format(self))

    def _make_unique_slug(self):
        queryset = self.__class__._default_manager
        slug = self._make_slug()
        try:
            initial_slug = slug
            queryset.get(slug=slug)
            i = 1
            while True:
                slug = '{0}-{1}'.format(initial_slug, i)
                queryset.get(slug=slug)
                i += 1

        except ObjectDoesNotExist:
            pass
        return slug

    def save(self, *args, **kwargs):
        if self.slug == '':
            self.slug = self._make_unique_slug()
        return super(SlugableModel, self).save(*args, **kwargs)
