# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rt_pie',
 'rt_pie.rt_pie_lib',
 'rt_pie.rt_pie_lib.config',
 'rt_pie.rt_pie_lib.converters',
 'rt_pie.rt_pie_lib.metrics',
 'rt_pie.rt_pie_lib.metrics.unvoiced_detector',
 'rt_pie.rt_pie_lib.networks']

package_data = \
{'': ['*']}

install_requires = \
['librosa>=0.8.0,<0.9.0',
 'matplotlib>=3.2,<3.3',
 'mir_eval>=0.6,<0.7',
 'numpy>=1.19,<1.20',
 'sounddevice>=0.4.1,<0.5.0',
 'tensorflow>=2.4.1,<3.0.0']

entry_points = \
{'console_scripts': ['rt_pie = rt_pie:main']}

setup_kwargs = {
    'name': 'rt-pie',
    'version': '0.1.10',
    'description': 'Real Rime PItch Estimator',
    'long_description': '# RT PIE<br>Real Time PItch Estimator\n\n[**pypi link**](https://pypi.org/project/rt-pie)\n\n## Installation\n\n    pip install rt_pie\n\n## Usage\n\n    from rt_pie import hello_world \n\n    hello_world.greet()\n\n## Development\n\nDownload sources\n\n    git clone ...\n\nInstall dependencies\n\n    poetry install\n\n### Build / Publish\n\n    poetry build\n    poetry publish --build [--dry-run]\n\n#### Authors\nKaspar Wolfisberg<br>\nLuca Di Lanzo\n\n',
    'author': 'Kaspar Wolfisberg',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/wolfisberg/rt-pie',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.8',
}


setup(**setup_kwargs)
