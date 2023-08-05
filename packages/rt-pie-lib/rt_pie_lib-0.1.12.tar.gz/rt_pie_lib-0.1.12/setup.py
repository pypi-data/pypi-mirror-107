# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rt_pie_lib',
 'rt_pie_lib.converters',
 'rt_pie_lib.metrics',
 'rt_pie_lib.metrics.unvoiced_detector']

package_data = \
{'': ['*']}

install_requires = \
['mir_eval>=0.6,<0.7', 'numpy>=1.19,<1.20', 'scipy>=1.6.3,<2.0.0']

setup_kwargs = {
    'name': 'rt-pie-lib',
    'version': '0.1.12',
    'description': 'Real Rime PItch Estimator Library',
    'long_description': None,
    'author': 'Kaspar Wolfisberg',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.8',
}


setup(**setup_kwargs)
