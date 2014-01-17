# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='PhotoFUSE',
    version='1.0',
    description="PhotoFUSE: Show photos based on ratings and tags",
    author='Tim Freund',
    author_email='tim@freunds.net',
    license = 'MIT License',
    url='http://github.com/timfreund/photofuse',
    install_requires=[
        'fusepy',
        # PIL
                ],
    packages=['photofuse'],
    include_package_data=True,
    entry_points="""
    [console_scripts]
    photofuse-ls = photofuse.cli:ls
    photofuse = photofuse.cli:photofuse
    """,
)
