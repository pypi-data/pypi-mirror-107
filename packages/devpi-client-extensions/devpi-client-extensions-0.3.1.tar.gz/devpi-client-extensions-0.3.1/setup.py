# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['devpi_ext']

package_data = \
{'': ['*']}

install_requires = \
['devpi-client>=3.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.5.0,<2.0.0'],
 'keyring': ['keyring']}

entry_points = \
{'devpi_client': ['devpi-client-ext-login-keyring = '
                  'devpi_ext.login:_keyring_plugin [keyring]',
                  'devpi-client-ext-login-pypirc = '
                  'devpi_ext.login:_pypirc_plugin']}

setup_kwargs = {
    'name': 'devpi-client-extensions',
    'version': '0.3.1',
    'description': 'devpi client extensions',
    'long_description': "devpi-client-extensions\n=======================\n\nSome useful stuff around `devpi client`_. Although this package is proudly named\n*extensions*, currently there is only one thing implemented ready to be used:\na hook that uses passwords from ``.pypirc`` or `keyring`_ on login to devpi server\nso you don't have to enter your password if you store it for upload anyway.\n\nInstall\n-------\n\n.. code-block:: sh\n\n   $ pip install devpi-client-extensions\n\nUsage\n-----\n\nJust use the ``devpi login`` command as usual:\n\n.. code-block:: sh\n\n   $ devpi login hoefling\n   Using hoefling credentials from .pypirc\n   logged in 'hoefling', credentials valid for 10.00 hours\n\nKeyring Support\n---------------\n\nSince version 0.3, reading credentials using `keyring`_ is supported.\nInstall the package with ``keyring`` extras:\n\n.. code-block:: sh\n\n   $ pip install devpi-client-extensions[keyring]\n\nExample with storing the password in keyring:\n\n.. code-block:: sh\n\n   $ keyring set https://my.devpi.url/ hoefling\n   $ devpi login hoefling\n   Using hoefling credentials from keyring\n   logged in 'hoefling', credentials valid for 10.00 hours\n\nStats\n-----\n\n|pypi| |build| |coverage| |requirements| |black|\n\n.. |pypi| image:: https://img.shields.io/pypi/v/devpi-client-extensions.svg?logo=python&logoColor=white\n   :target: https://pypi.python.org/pypi/devpi-client-extensions\n   :alt: Package on PyPI\n\n.. |build| image:: https://github.com/hoefling/devpi-client-extensions/workflows/CI/badge.svg\n   :target: https://github.com/hoefling/devpi-client-extensions/actions?query=workflow%3A%22CI%22\n   :alt: Build status on Github Actions\n\n.. |coverage| image:: https://codecov.io/gh/hoefling/devpi-client-extensions/branch/master/graph/badge.svg\n   :target: https://codecov.io/gh/hoefling/devpi-client-extensions\n   :alt: Coverage status\n\n.. |requirements| image:: https://requires.io/github/hoefling/devpi-client-extensions/requirements.svg?branch=master\n   :target: https://requires.io/github/hoefling/devpi-client-extensions/requirements/?branch=master\n   :alt: Requirements status\n\n.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/ambv/black\n\n.. _devpi client: https://pypi.org/project/devpi-client/\n\n.. _keyring: https://pypi.org/project/keyring/\n",
    'author': 'Oleg Höfling',
    'author_email': 'oleg.hoefling@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hoefling/devpi-client-extensions',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
