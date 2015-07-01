# -*- coding: utf-8 -*-

from pickle import dumps

from django.db import models


class CacheManager(models.Manager):

    def __init__(self):
        self.cache = {}
        self.name = 'cache-manager'

    def _get_cache_key(self, **kwargs):
        args = kwargs.copy()
        if 'defaults' in args:
            del(args['defaults'])
        return self.model.__module__ + self.model.__name__ + dumps(args)

    def get(self, **kwargs):
        cache_key = self._get_cache_key(**kwargs)
        if cache_key not in self.cache:
            self.cache[cache_key] = super(CacheManager, self).get(**kwargs)
        return self.cache[cache_key]

    def get_or_create(self, **kwargs):
        cache_key = self._get_cache_key(**kwargs)
        if cache_key not in self.cache:
            self.cache[cache_key] = super(CacheManager, self).get_or_create(**kwargs)
        return self.cache[cache_key]

    def get_all_by_key(self, key):
        return {getattr(obj, key): obj for obj in self.all()}
