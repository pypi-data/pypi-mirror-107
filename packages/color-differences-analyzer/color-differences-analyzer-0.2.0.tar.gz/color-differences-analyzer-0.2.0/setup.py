# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['color_differences_analyzer']

package_data = \
{'': ['*']}

install_requires = \
['colormath>=3.0.0,<4.0.0',
 'matplotlib>=3.4.2,<4.0.0',
 'numpy>=1.20.3,<2.0.0',
 'openpyxl>=3.0.7,<4.0.0',
 'pandas>=1.2.4,<2.0.0',
 'scikit-image>=0.18.1,<0.19.0',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['cda = color_differences_analyzer.main:app']}

setup_kwargs = {
    'name': 'color-differences-analyzer',
    'version': '0.2.0',
    'description': 'Command line interface to analyze differences of colors from images implemented with Python.',
    'long_description': '# Color Differences Analyzer\n\n[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)\n[![Test](https://github.com/leynier/color-differences-analyzer/workflows/CI/badge.svg)](https://github.com/leynier/color-differences-analyzer/actions?query=workflow%3ACI)\n[![codecov](https://codecov.io/gh/leynier/color-differences-analyzer/branch/main/graph/badge.svg?token=Z1MEEL3EAB)](https://codecov.io/gh/leynier/color-differences-analyzer)\n[![DeepSource](https://deepsource.io/gh/leynier/color-differences-analyzer.svg/?label=active+issues)](https://deepsource.io/gh/leynier/color-differences-analyzer/?ref=repository-badge)\n[![Version](https://img.shields.io/pypi/v/color-differences-analyzer?color=%2334D058&label=Version)](https://pypi.org/project/color-differences-analyzer)\n[![Last commit](https://img.shields.io/github/last-commit/leynier/color-differences-analyzer.svg?style=flat)](https://github.com/leynier/color-differences-analyzer/commits)\n[![GitHub commit activity](https://img.shields.io/github/commit-activity/m/leynier/color-differences-analyzer)](https://github.com/leynier/color-differences-analyzer/commits)\n[![Github Stars](https://img.shields.io/github/stars/leynier/color-differences-analyzer?style=flat&logo=github)](https://github.com/leynier/color-differences-analyzer/stargazers)\n[![Github Forks](https://img.shields.io/github/forks/leynier/color-differences-analyzer?style=flat&logo=github)](https://github.com/leynier/color-differences-analyzer/network/members)\n[![Github Watchers](https://img.shields.io/github/watchers/leynier/color-differences-analyzer?style=flat&logo=github)](https://github.com/leynier/color-differences-analyzer)\n[![Website](https://img.shields.io/website?up_message=online&url=https%3A%2F%2Fleynier.github.io/color-differences-analyzer)](https://leynier.github.io/color-differences-analyzer)\n[![GitHub contributors](https://img.shields.io/github/contributors/leynier/color-differences-analyzer)](https://github.com/leynier/color-differences-analyzer/graphs/contributors)\n\nCommand line interface to analyze differences of colors from images implemented with Python.\n',
    'author': 'Leynier Gutiérrez González',
    'author_email': 'leynier41@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/leynier/color-differences-analyzer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
