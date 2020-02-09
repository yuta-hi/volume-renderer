#!/usr/bin/env python

from setuptools import find_packages
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='pyvr',
    version='1.0.0',
    description='Volume Renderer with VTK',
    long_description=open('README.md').read(),
    author='yuta-hi',
    packages=find_packages(),
    include_package_data=True,
    scripts=[],
    install_requires=open('requirements.txt').readlines(),
    url='https://github.com/yuta-hi/volume-renderer',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
)
