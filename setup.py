from setuptools import setup, find_packages

setup(
    name='django-basic-models-behaviors',
    version=__import__('basic_models_behaviors').__version__,
    description='',
    author='Nicolas Dubois',
    author_email='nicolas.c.dubois@gmail.com',
    url='https://github.com/duboisnicolas/django-basic-models-behaviors',
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
