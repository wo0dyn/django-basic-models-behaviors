# -*- coding: utf-8 -*-

import codecs
import os

from setuptools import setup


def read(*parts):
    return codecs.open(os.path.join(os.path.dirname(__file__), *parts), encoding='utf-8').read()

setup(
    name='django-basic-models-behaviors',
    version=__import__('basic_models_behaviors').__version__,
    description='Tiny app to provide basic behaviors for django models.',
    long_description=read('README.rst'),
    author='Nicolas Dubois',
    author_email='nicolas.c.dubois@gmail.com',
    url='https://github.com/duboisnicolas/django-basic-models-behaviors',
    keywords="django",
    packages=['basic_models_behaviors'],
    include_package_data=True,
    zip_safe=False,
    license='MIT License',
    platforms=['any'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ]
)
