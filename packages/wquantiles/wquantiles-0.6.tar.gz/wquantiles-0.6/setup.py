# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['wquantiles', 'weighted']
install_requires = \
['numpy>=1.18']

setup_kwargs = {
    'name': 'wquantiles',
    'version': '0.6',
    'description': 'Weighted quantiles, including weighted median, based on numpy',
    'long_description': None,
    'author': 'Jose Sabater',
    'author_email': 'jsm@jsabater.info',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://github.com/nudomarinero/wquantiles/',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
