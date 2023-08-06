# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['verlat']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.8.2,<2.0.0', 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'verlat',
    'version': '0.1.0.post1',
    'description': 'Get info about the latest release of a package on PyPI.',
    'long_description': '# verlat\n\nGet info about the latest release of a package on PyPI.\n\n[![Code Quality](https://github.com/aahnik/verlat/actions/workflows/quality.yml/badge.svg)](https://github.com/aahnik/verlat/actions/workflows/quality.yml)\n[![Tests](https://github.com/aahnik/verlat/actions/workflows/test.yml/badge.svg)](https://github.com/aahnik/verlat/actions/workflows/test.yml)\n[![codecov](https://codecov.io/gh/aahnik/verlat/branch/main/graph/badge.svg?token=RO18ZS775L)](https://codecov.io/gh/aahnik/verlat)\n\n## Installation\n\n```shell\npip install verlat\n```\n\n## Usage\n\n```python\nfrom verlat import latest_release\n\nrelease = latest_release("verlat")\n\nprint(release.version)\n```\n',
    'author': 'aahnik',
    'author_email': 'daw@aahnik.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aahnik/verlat',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
