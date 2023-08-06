# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_github_tags', 'django_github_tags.templatetags']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'django-github-tags',
    'version': '1.0.0',
    'description': 'Access to GitHub API using tags in your Django templates.',
    'long_description': None,
    'author': 'PabloLec',
    'author_email': 'pablo.lecolinet@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
