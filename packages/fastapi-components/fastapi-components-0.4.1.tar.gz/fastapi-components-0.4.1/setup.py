# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_components', 'fastapi_components.components']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.5,<0.6', 'pydantic[dotenv]>=1.7,<2.0']

extras_require = \
{'aiohttp': ['aiohttp>=3.7.3,<4.0.0'],
 'all': ['aiopg>=1.1,<2.0',
         'aioredis>=1.3,<2.0',
         'aiokafka>=0.7,<0.8',
         'uvicorn[uvloop]>=0.13,<0.14',
         'fastapi>=0.63,<0.64',
         'sqlalchemy>=1.3.24,<1.4.0',
         'motor>=2.3.1,<3.0.0',
         'aiohttp>=3.7.3,<4.0.0'],
 'kafka': ['aiokafka>=0.7,<0.8'],
 'mongo': ['motor>=2.3.1,<3.0.0'],
 'postgres': ['aiopg>=1.1,<2.0', 'sqlalchemy>=1.3.24,<1.4.0'],
 'redis': ['aioredis>=1.3,<2.0'],
 'web': ['uvicorn[uvloop]>=0.13,<0.14', 'fastapi>=0.63,<0.64']}

setup_kwargs = {
    'name': 'fastapi-components',
    'version': '0.4.1',
    'description': 'This library makes it easy to add dependencies to your fastapi service',
    'long_description': None,
    'author': 'Dmitriy Troyan',
    'author_email': 'kashil.dima@yandex.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
