# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['calls']

package_data = \
{'': ['*']}

install_requires = \
['typing-extensions>=3.7.4,<4.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1,<5']}

setup_kwargs = {
    'name': 'calls',
    'version': '0.1.1',
    'description': 'Utilities for callables',
    'long_description': "🤙 Calls\n========\n\n.. image:: https://img.shields.io/pypi/v/calls.svg?style=flat-square\n   :target: https://pypi.python.org/pypi/calls\n\n.. image:: https://img.shields.io/pypi/l/calls.svg?style=flat-square\n   :target: https://pypi.python.org/pypi/calls\n\n.. image:: https://img.shields.io/pypi/pyversions/calls.svg?style=flat-square\n   :target: https://pypi.python.org/pypi/calls\n\n.. image:: https://img.shields.io/readthedocs/calls.svg?style=flat-square\n   :target: http://calls.readthedocs.io/\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square\n   :target: https://github.com/psf/black\n\nSimple, typed, composable tools for callables.\n\nQuickstart\n----------\n\nAll utilities are directly importable.\nSee `the docs <https://calls.rtfd.io>`_ for a complete overview.\n\n.. code-block:: python\n\n  >>> from calls import raises, const, identity, flip\n\nInstallation\n------------\n\nIt's available on PyPI.\n\n.. code-block:: bash\n\n  pip install calls\n",
    'author': 'Arie Bovenberg',
    'author_email': 'a.c.bovenberg@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ariebovenberg/calls',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
