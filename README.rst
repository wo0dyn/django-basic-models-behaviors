==============================
Django: Basic Models Behaviors
==============================

.. image:: https://img.shields.io/pypi/v/django-basic-models-behaviors.svg
    :target: https://pypi.python.org/pypi/django-basic-models-behaviors/
    :alt: Latest Version on PyPI

.. image:: https://img.shields.io/pypi/pyversions/django-basic-models-behaviors.svg
    :target: https://pypi.python.org/pypi/django-basic-models-behaviors/
    :alt: Supported Python versions

.. image:: https://img.shields.io/travis/wo0dyn/django-basic-models-behaviors.svg
    :target: https://travis-ci.org/wo0dyn/django-basic-models-behaviors
    :alt: TravisCI status

Tiny app to provide basic behaviors for django models, like:

* Timestampable
* Publishable
* SoftDeletable
* Cacheable

Installation
------------

From PyPI::

    $ pip install django-basic-models-behaviors

Usage
-----

PublishableModel
~~~~~~~~~~~~~~~~

Here is an example of Article using *PublishableModel*:

.. code-block:: python

    from basic_models_behaviors import models as behaviors
    from django.db import models

    class Article(behaviors.PublishableModel):
        title = models.CharField(max_length=255)
        contents = models.TextField()

Then:

.. code-block:: python

    >>> article = Article(title='Foo', contents='Lorem lipsum')
    >>> article.publish()
    >>> article.is_published()
    True
    >>> article.unpublish()
    >>> article.is_published()
    False
    >>> article.is_not_published()
    True


SoftDeletableModel
~~~~~~~~~~~~~~~~~~

SoftDeletableModel behavior will add deleted_at field in set the current
timestamp instead of delete the object.
force_delete() will actually delete the model.

In your models.py:

.. code-block:: python

    from basic_models_behaviors import models as behaviors
    from django.db import models

    class Article(behaviors.SoftDeletableModel):
        title = models.CharField(max_length=255)
        contents = models.TextField()

Then:

.. code-block:: python

    >>> from models import Article
    >>> article = Article(title='foo', contents='Lorem lipsum')
    >>> article.delete()
    >>> article.has_been_deleted()
    True
    >>> article.undelete()
    >>> article.has_been_deleted()
    False
    >>> article.force_delete()

Tests
-----

Run tests::

    $ pip install -r tests/requirements.txt
    $ py.test --ds=tests.settings tests

Authors
-------

* `@wo0dyn <https://github.com/wo0dyn>`_ • Nicolas Dubois <nicolas.c.dubois@gmail.com>
