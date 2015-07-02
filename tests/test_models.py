# -*- coding: utf-8 -*-

from django.test import TestCase
from django.core.cache import cache

from .models import PublishableMock, SoftDeletableMock, TimestampableMock, CacheableMock
from basic_models_behaviors.managers import get_key_for_instance


class PublishableTest(TestCase):

    def setUp(self):
        self.pm = PublishableMock()

    def test_publish(self):
        self.pm.publish()
        self.assert_(self.pm.published_at is not None)

    def test_published_at(self):
        self.pm.publish()
        self.assert_(self.pm.published_at is not None)
        self.pm.unpublish()
        self.assert_(self.pm.published_at is None)


class SoftDeletableTest(TestCase):

    def setUp(self):
        self.sdm = SoftDeletableMock()
        self.sdm.save()

    def test_deleted_at(self):
        self.sdm.delete()
        self.assert_(self.sdm is not None)
        self.assert_(self.sdm.deleted_at is not None)
        self.sdm.undelete()
        self.assert_(self.sdm.deleted_at is None)

    def test_force_delete(self):
        self.assert_(self.sdm.id is not None)
        self.sdm.force_delete()
        self.assert_(self.sdm.id is None)


class TimestampableModelTests(TestCase):

    def setUp(self):
        self.tm1 = TimestampableMock.objects.create()
        self.tm2 = TimestampableMock.objects.create()

    def test_created_at(self):
        self.assert_(self.tm2.created_at > self.tm1.created_at)

    def test_updated_at(self):
        self.tm1.save()
        self.assert_(self.tm2.updated_at < self.tm1.updated_at)


class CacheableModelTests(TestCase):

    def setUp(self):
        cache.clear()

    def test_instance_is_cached_after_saving(self):
        cm = CacheableMock()
        cm.save()
        key = get_key_for_instance(cm)
        self.assertEqual(cache.get(key), cm)

    def test_instance_is_cached_after_create(self):
        cm = CacheableMock.objects.create()
        key = get_key_for_instance(cm)
        self.assertEqual(cache.get(key), cm)

    def test_instance_is_cached_after_get_or_create(self):
        cm, created = CacheableMock.objects.get_or_create()
        self.assertTrue(created)
        key = get_key_for_instance(cm)
        self.assertEqual(cache.get(key), cm)

    def test_instance_is_uncached_after_delete(self):
        cm = CacheableMock.objects.create()
        key = get_key_for_instance(cm)
        cm.delete()
        self.assertIsNone(cache.get(key))

    def test_multiple_instances(self):
        cm1 = CacheableMock.objects.create()
        cm2 = CacheableMock.objects.create()
        cm3 = CacheableMock.objects.create()
        cm2.delete()
        key = get_key_for_instance(cm1)
        self.assertEqual(cache.get(key), cm1)
        key = get_key_for_instance(cm3)
        self.assertEqual(cache.get(key), cm3)

    def test_queries_count_after_saving_and_filter(self):
        with self.assertNumQueries(1):
            self.test_instance_is_cached_after_saving()
            cm = CacheableMock.objects.filter(pk=1)
            self.assertEqual(len(cm), 1)

    def test_queries_count_after_saving_and_get(self):
        with self.assertNumQueries(1):
            self.test_instance_is_cached_after_saving()
            cm = CacheableMock.objects.get(pk=1)
            self.assertEqual(len(cm), 1)

    def test_queries_count_after_create_and_filter(self):
        with self.assertNumQueries(1):
            self.test_instance_is_cached_after_create()
            cm = CacheableMock.objects.filter(pk=1)
            self.assertEqual(len(cm), 1)

    def test_queries_count_after_create_and_get(self):
        with self.assertNumQueries(1):
            self.test_instance_is_cached_after_create()
            cm = CacheableMock.objects.get(pk=1)
            self.assertEqual(len(cm), 1)

    def test_queries_count_after_get_or_create_and_filter(self):
        """ 4 queries here, because of transaction SAVEPOINT """
        with self.assertNumQueries(4):
            self.test_instance_is_cached_after_get_or_create()
            cm = CacheableMock.objects.filter(pk=1)
            self.assertEqual(len(cm), 1)

    def test_queries_count_after_get_or_create_and_get(self):
        """ 4 queries here, because of transaction SAVEPOINT """
        with self.assertNumQueries(4):
            self.test_instance_is_cached_after_get_or_create()
            cm = CacheableMock.objects.get(pk=1)
            self.assertEqual(len(cm), 1)

    def test_multiple_objects_returned_with_filters(self):
        with self.assertNumQueries(3):
            CacheableMock.objects.create()
            CacheableMock.objects.create()
            CacheableMock.objects.create()
            cms = CacheableMock.objects.filter(pk__in=[1, 3])
            self.assertEqual(len(cms), 2)
            cm = CacheableMock.objects.filter(pk=1)
            self.assertEqual(len(cm), 1)
