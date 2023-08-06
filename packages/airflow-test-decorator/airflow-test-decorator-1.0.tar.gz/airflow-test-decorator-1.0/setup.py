# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['airflow_test_decorator']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.3,<1.4',
 'apache-airflow==1.10.15',
 'cattrs==1.0.0',
 'presto-python-client>=0.7.0,<0.8.0']

setup_kwargs = {
    'name': 'airflow-test-decorator',
    'version': '1.0',
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
