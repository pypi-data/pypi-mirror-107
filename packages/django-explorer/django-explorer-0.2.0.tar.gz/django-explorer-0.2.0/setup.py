# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_explorer',
 'django_explorer.templatetags',
 'django_explorer.templatetags.themes',
 'django_explorer.themes']

package_data = \
{'': ['*'], 'django_explorer': ['templates/django_explorer/*']}

install_requires = \
['django>=3,<4', 'pydantic>=1.8.2,<2.0.0', 'python-magic>=0.4.22,<0.5.0']

extras_require = \
{':python_version >= "3.7"': ['ipython>=7.0.0,<8.0.0']}

setup_kwargs = {
    'name': 'django-explorer',
    'version': '0.2.0',
    'description': 'Serve local direcotry listing from django',
    'long_description': '# django_explorer\n\nServe local direcotry listing from your django app\n\nTODO: context type with field mapping constants\n\n## Demo app\n\n1. Install dependencies `poetry install`\n2. Run demo app `make run_demo_app` (`make run_demo_app port=8888` if you want to use custom port)\n',
    'author': 'dhvcc',
    'author_email': '1337kwiz@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dhvcc/django_explorer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.2,<4',
}


setup(**setup_kwargs)
