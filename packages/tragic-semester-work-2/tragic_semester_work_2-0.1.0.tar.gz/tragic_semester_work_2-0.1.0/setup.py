# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tragic_semester_work_2']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0', 'unittest>=0.0,<0.1']

setup_kwargs = {
    'name': 'tragic-semester-work-2',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Пётр Куркин',
    'author_email': 'kurkin801@mail.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
