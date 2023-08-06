# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['web_crawler',
 'web_crawler.models',
 'web_crawler.services',
 'web_crawler_cli',
 'web_crawler_cli.commands']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2', 'requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['web_crawler = web_crawler_cli.web_crawler_cli:cli']}

setup_kwargs = {
    'name': 'py-webcrawler',
    'version': '0.1.0',
    'description': 'python web crawler',
    'long_description': None,
    'author': 'Patricio Tula',
    'author_email': 'tula.patricio@gmail.com',
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
