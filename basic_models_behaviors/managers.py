# -*- coding: utf-8 -*-

from django.db import models
from pickle import dumps

class CacheManager(models.Manager):
    cache = {}
    
    def _get_cache_key(self, **kwargs):
        args = kwargs.copy()
        if 'defaults' in args:
            del(args['defaults'])
        return self.model.__module__ + self.model.__name__ + dumps(args)
    
    # TODO: refactoring on get() and get_or_create()!!
    
    def get(self, **kwargs):
        cache_key = self._get_cache_key(**kwargs)
        if not self.cache.has_key(cache_key):
            self.cache[cache_key] = super(CacheManager, self).get(**kwargs)
        return self.cache[cache_key]
    
    def get_or_create(self, **kwargs):
        cache_key = self._get_cache_key(**kwargs)
        if not self.cache.has_key(cache_key):
            self.cache[cache_key] = super(CacheManager, self).get_or_create(**kwargs)
        return self.cache[cache_key]

    def get_all_by_key(self, key):
        objects = {}
        for obj in self.all():
                objects[getattr(obj, key)] = obj
        return objects
