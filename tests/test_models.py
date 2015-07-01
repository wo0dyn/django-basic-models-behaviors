# -*- coding: utf-8 -*-

from django.test import TestCase

from .models import PublishableMock, SoftDeletableMock, TimestampableMock


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
