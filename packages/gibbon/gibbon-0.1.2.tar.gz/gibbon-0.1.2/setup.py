# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gibbon']

package_data = \
{'': ['*']}

install_requires = \
['tqdm>=4.59.0,<5.0.0']

entry_points = \
{'console_scripts': ['gibbon = gibbon.__main__:main']}

setup_kwargs = {
    'name': 'gibbon',
    'version': '0.1.2',
    'description': '',
    'long_description': '# `gibbon`\n\n[![pypi version](https://img.shields.io/pypi/v/gibbon.svg?style=flat)](https://pypi.org/pypi/gibbon/)\n[![downloads](https://pepy.tech/badge/gibbon)](https://pepy.tech/project/gibbon)\n[![build status](https://github.com/dawsonbooth/gibbon/workflows/build/badge.svg)](https://github.com/dawsonbooth/gibbon/actions?workflow=build)\n[![python versions](https://img.shields.io/pypi/pyversions/gibbon.svg?style=flat)](https://pypi.org/pypi/gibbon/)\n[![format](https://img.shields.io/pypi/format/gibbon.svg?style=flat)](https://pypi.org/pypi/gibbon/)\n[![license](https://img.shields.io/pypi/l/gibbon.svg?style=flat)](https://github.com/dawsonbooth/gibbon/blob/master/LICENSE)\n\n## Description\n\nOrganize the files in your filesystem according to their attributes.\n\n## Installation\n\nWith [Python](https://www.python.org/downloads/) installed, simply run the following command to add the package to your project.\n\n```bash\npython -m pip install gibbon\n```\n\n## Usage\n\nThe following is an example usage of the package:\n\n```python\nfrom gibbon import Tree\n\nwith Tree("/path/to/root/folder/", glob="**/*.txt") as tree:\n    tree.flatten()\n```\n\nFeel free to [check out the docs](https://dawsonbooth.github.io/gibbon/) for more information.\n\n## License\n\nThis software is released under the terms of [MIT license](LICENSE).\n',
    'author': 'Dawson Booth',
    'author_email': 'pypi@dawsonbooth.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dawsonbooth/gibbon',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
