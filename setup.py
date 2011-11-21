from setuptools import setup, find_packages

setup(
    name='django-basic-models-behaviors',
    version='0.2.0',
    description='',
    author='Nicolas Dubois',
    author_email='nicolas.c.dubois@gmail.com',
    url='http://hg.nicolasdubois.com/django-basic-models-behaviors',
    keywords = "django",
    packages=['basic_models_behaviors'],
    include_package_data=True,
    zip_safe=False,
    license='MIT License',
    platforms = ['any'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ]
)
