# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_github_tags', 'django_github_tags.templatetags']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'django-github-tags',
    'version': '0.1.0',
    'description': 'Access to GitHub API using tags in your Django templates.',
    'long_description': None,
    'author': 'PabloLec',
    'author_email': 'pablo.lecolinet@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
