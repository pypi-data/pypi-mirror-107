# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['airflow_snapshot_test']

package_data = \
{'': ['*']}

install_requires = \
['apache-airflow==1.10.15', 'presto-python-client>=0.7.0,<0.8.0']

setup_kwargs = {
    'name': 'airflow-snapshot-test',
    'version': '0.1.6',
    'description': '',
    'long_description': None,
    'author': 'komalkot',
    'author_email': 'komalkot@thoughtworks.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
