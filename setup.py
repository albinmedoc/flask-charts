# -*- coding: utf-8 -*-
"""
Flask-Charts
-------------

Easily add google charts to Flask templates
"""
from setuptools import setup
setup(
    name='Flask-Charts',
    version='1.5',
    url='https://github.com/albinmedoc/flask-charts',
    license='MIT',
    author='Albin Médoc',
    author_email='stamline203@gmail.com',
    description='Google Charts API support for Flask',
    long_description=__doc__,
    packages=['flask_charts'],
    package_data={
        'flask_charts': [
            'templates/*',
            'static/*']
        },
    py_modules=['flask_charts'],
    zip_safe=False,
    platforms='any',
    install_requires=['Flask'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: JavaScript',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
