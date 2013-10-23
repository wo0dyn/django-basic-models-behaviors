Django: Basic Models Behaviors
==============================

django-basic-models-behaviors is a tiny app to provide basic behaviors like:

* Timestampable
* Publishable
* SoftDeletable
* Cacheable

Installation
------------

Ok, so far: you're crazy! But here is the way you can install this app::

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

    $ cd tests && python manage.py test

Authors
-------

Nicolas Dubois <nicolas.c.dubois@gmail.com>
