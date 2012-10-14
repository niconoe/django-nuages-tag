# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages

setup(
    name='django-nuages-tag',
    version='0.1.2',
    author=u'Nicolas Noé',
    author_email='nicolas@niconoe.eu',
    packages=find_packages(),
    url='https://github.com/niconoe/django-nuages-tag/',
    license='BSD licence, see LICENCE.txt',
    description='A simple Django TemplateTag (named compute_tag_cloud) to help in the creation of tag clouds.',
    long_description=open('README.rst').read(),
    include_package_data=True,
    zip_safe=False,
)
