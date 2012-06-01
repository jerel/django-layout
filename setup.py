#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='{{ project_name }}',
    version='1.0',
    description="",
    author="nGen Works",
    author_email='info@ngenworks.com',
    url='',
    packages=find_packages(),
    package_data={'{{ project_name }}': ['static/*.*', 'templates/*.*']},
    scripts=['manage.py'],
)
