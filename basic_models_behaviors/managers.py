# -*- coding: utf-8 -*-
#
from django.db import models
from django.core.cache import cache
from django.db.models.query import QuerySet


class CachedQuerySet(QuerySet):

    def get_pk(self, kwargs):
        for val in ('pk', 'pk__exact', 'id', 'id__exact'):
            if val in kwargs:
                return kwargs[val]
        return None

    def get_pks(self, kwargs):
        for val in ('pk__in', 'id__in'):
            if val in kwargs:
                return kwargs[val]
        return None

    def get_all_pks(self, kwargs):
        pks = []
        for val in ('pk', 'pk__exact', 'id', 'id__exact', 'pk__in', 'id__in'):
            if val in kwargs:
                pks = kwargs[val] if type(kwargs[val]) is list else [kwargs[val]]
        if len(pks) > 0:
            return pks
        return None

    def filter(self, *args, **kwargs):
        pks = self.get_all_pks(kwargs)
        if pks is not None:
            self._result_cache = []
            for pk in pks:
                key = get_key_for_instance(self.model, pk=pk)
                cache_content = cache.get(key)
                if cache_content is not None:
                    self._result_cache.append(cache_content)
            if len(self._result_cache) > 0:
                return self
        return super(CachedQuerySet, self).filter(*args, **kwargs)

    def get(self, *args, **kwargs):
        pk = self.get_pk(kwargs)
        if pk is not None:
            clone = self.filter(*args, **kwargs)
            if self._result_cache is not None and len(self._result_cache) > 0:
                return clone[0]
        return super(CachedQuerySet, self).get(*args, **kwargs)


class CacheManager(models.Manager):

    def get_queryset(self):
        return CachedQuerySet(self.model)


def get_key_for_instance(instance, pk=None):
    return '{label}.{module}:{pk}'.format(
        label=instance._meta.app_label,
        module=instance._meta.model_name,
        pk=instance.pk if pk is None else pk)
