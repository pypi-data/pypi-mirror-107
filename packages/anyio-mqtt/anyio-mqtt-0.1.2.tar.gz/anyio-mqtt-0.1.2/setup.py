# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['anyio_mqtt']
install_requires = \
['anyio>=3.0.1,<4.0.0', 'paho-mqtt>=1.5.1,<2.0.0']

setup_kwargs = {
    'name': 'anyio-mqtt',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'Ellis Percival',
    'author_email': 'anyio-mqtt@failcode.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
