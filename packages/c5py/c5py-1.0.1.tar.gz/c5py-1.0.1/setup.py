# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['c5',
 'c5.corpus',
 'c5.derived',
 'c5.dl',
 'c5.elan',
 'c5.raw',
 'c5.tools',
 'c5.tools.sync',
 'c5.tools.sync.control',
 'c5.tools.sync.gui',
 'c5.tools.sync.model',
 'c5.tools.sync.tools']

package_data = \
{'': ['*'],
 'c5': ['viewer/*', 'viewer/css/*', 'viewer/js/*'],
 'c5.tools.sync': ['data/*', 'img/*']}

install_requires = \
['BeautifulSoup4>=4.9,<5.0',
 'Twisted>=20.3.0,<21.0.0',
 'lxml>=4.6,<5.0',
 'matplotlib>=3.3,<3.4',
 'pandas>=1.1.5,<1.2.0',
 'scikit-learn>=0.23,<0.24',
 'scipy>=1.6.0,<1.7.0',
 'seaborn>=0.11,<0.12',
 'service_identity>=18.1.0,<19.0.0',
 'tables>=3.6,<4.0']

entry_points = \
{'console_scripts': ['c5helper = c5.tools.helper:start_app',
                     'c5sync = c5.tools.sync.startup:start_app',
                     'c5viewer = c5.tools.dataviewer:start_app']}

setup_kwargs = {
    'name': 'c5py',
    'version': '1.0.1',
    'description': "Analysis and visualization tools for the Augmented Reality-based Corpus (ARbC). This corpus has been created in the research project 'Alignment in AR-based cooperation' which was a part of the Collaborative Research Centre 'Alignment in Communication' (CRC 673) under the project code C5.",
    'long_description': '# c5py\n',
    'author': 'Alexander Neumann',
    'author_email': 'alneuman@techfak.uni-bielefeld.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://wwwhomes.uni-bielefeld.de/sfb-673/projects/C5',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
