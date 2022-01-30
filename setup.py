import os
from setuptools import setup, find_packages

setup(
    name='pycbor-extra',
    version=os.environ.get('version', '0'),
    description='encoding/decoding of extra types',
    url='ssh://git@ids:textapp/pycbor-extra',
    author='dvzubarev',
    author_email='zubarev@isa.ru',
    license='MIT',
    packages=find_packages(),
    install_requires=['cbor2', 'numpy'],
)
