# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['machine_data_hub']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0',
 'rfc6266>=0.0.4,<0.0.5',
 'sphinx-rtd-theme>=0.5.1,<0.6.0',
 'tabulate>=0.8.9,<0.9.0',
 'tqdm>=4.60.0,<5.0.0',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['mdh = machine_data_hub.cli:main']}

setup_kwargs = {
    'name': 'machine-data-hub',
    'version': '0.1.1',
    'description': 'Python-based Command Line Tool to use the Machine Data Hub',
    'long_description': '[![Documentation Status](https://readthedocs.org/projects/machine-data-hub/badge/?version=latest)](https://machine-data-hub.readthedocs.io/en/latest/?badge=latest)\n\n# Machine Data Hub\nPython Client to use the [Machine Data Hub](https://machinedatahub.ai), an open source project\nto make state of the art machine learning and artificial intelligence techniques more accessible to engineering domains \nby providing suitable benchmark datasets for advancing prognostics\n',
    'author': 'ceciliabarnes',
    'author_email': 'cbarnes7@uw.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://machinedatahub.ai/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
