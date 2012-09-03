# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
 
long_description = open('README.md').read()
 
setup(
  name='django-parse_rss',
  version='1.0',
  description='Django rss reader',
  long_description=long_description,
  author='Frank van der Pluijm',
  author_email='f.vd.pluijm@hub.nl',
  url='https://github.com/frankvdp/django-parse_rss',
  packages=(
    'flag',
    'flag.templatetags',
  ),
  zip_safe=False,
)