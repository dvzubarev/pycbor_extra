from setuptools import (
    setup,
)

setup(
    name='cbor-extra',
    version='0.1',
    description='encoding/decoding of extra types',
    url='http://ids.isa.ru:8083/git/textapp/pycbor-extra',
    author='dvzubarev',
    author_email='zubarev@isa.ru',
    license='MIT',
    packages=['cbor_extra'],
    install_requires=['cbor2', 'numpy'],
)
