# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kociemba']

package_data = \
{'': ['*'], 'kociemba': ['tables/*']}

setup_kwargs = {
    'name': 'kociemba-manim-rubikscube',
    'version': '0.0.1',
    'description': '',
    'long_description': "This had to be uploaded to PyPI because manim-rubikscube depends on this package and PyPI won't allow a direct dependency to GitHub.",
    'author': 'Name',
    'author_email': 'fake-noreply@email.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/WampyCakes/kociemba',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
