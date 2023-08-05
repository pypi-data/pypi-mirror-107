# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['baguette_bi',
 'baguette_bi.cli',
 'baguette_bi.core',
 'baguette_bi.core.connections',
 'baguette_bi.examples',
 'baguette_bi.examples.altair_examples',
 'baguette_bi.examples.altair_examples.case_studies',
 'baguette_bi.examples.altair_examples.other',
 'baguette_bi.server',
 'baguette_bi.server.api',
 'baguette_bi.server.schema',
 'baguette_bi.server.static',
 'baguette_bi.server.templates',
 'baguette_bi.server.views']

package_data = \
{'': ['*'],
 'baguette_bi.server.static': ['css/*', 'fonts/*', 'js/*'],
 'baguette_bi.server.templates': ['elements/*']}

install_requires = \
['Jinja2>=3.0.1,<4.0.0',
 'SQLAlchemy>=1.4.15,<2.0.0',
 'aiofiles>=0.7.0,<0.8.0',
 'altair>=4.1.0,<5.0.0',
 'fastapi>=0.65.1,<0.66.0',
 'itsdangerous>=2.0.1,<3.0.0',
 'psycopg2-binary>=2.8.6,<3.0.0',
 'typer>=0.3.2,<0.4.0',
 'uvicorn>=0.13.4,<0.14.0',
 'vega-datasets>=0.9.0,<0.10.0']

entry_points = \
{'console_scripts': ['baguette = baguette_bi.cli:app']}

setup_kwargs = {
    'name': 'baguette-bi',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'Mikhail Akimov',
    'author_email': 'rovinj.akimov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
