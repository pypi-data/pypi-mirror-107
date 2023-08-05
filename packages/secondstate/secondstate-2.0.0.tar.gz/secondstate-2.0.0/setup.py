# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['secondstate']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'secondstate',
    'version': '2.0.0',
    'description': 'Utility for generating datetimes within given constraints',
    'long_description': '# secondstate\n\n[![GitHub release](https://img.shields.io/github/release/fruiti-ltd/secondstate.svg)](https://gitHub.com/fruiti-ltd/secondstate/releases/)\n[![PyPI version](https://badge.fury.io/py/secondstate.svg)](https://badge.fury.io/py/secondstate)\n[![GitHub pull-requests](https://img.shields.io/github/issues-pr/fruiti-ltd/secondstate.svg)](https://gitHub.com/fruiti-ltd/secondstate/pull/)\n![Build](https://github.com/fruiti-ltd/secondstate/actions/workflows/build.yml/badge.svg)\n![Release](https://github.com/fruiti-ltd/secondstate/actions/workflows/release.yml/badge.svg)\n[![GitHub license](https://img.shields.io/github/license/fruiti-ltd/secondstate.svg)](https://github.com/fruiti-ltd/blob/main/LICENSE)\n\n## Requirements\n\n- Python >= 3.8\n- [Docker](https://docker.com) (for development only)\n\n## Installation\n\n    pip install secondstate\n\n## Usage\n\nLets say you want to figure out the availability of a haircut with a particular barber:\n\n```python\nfrom secondstate import SecondState\n\n# We want all available appointments from now until the next 7 days\nbarber = SecondState(start="2021-05-23T11:17:49", finish="2021-05-30T11:17:49")\n\n# The barber works Monday 10:00-16:00\nbarber.set(start="2021-05-24T10:00:00", finish="2021-05-24T16:00:00")\n\n# Looks like the barber already has appointments on Monday at 10:30 and 15:00\nbarber.unset(start="2021-05-24T10:30:00", finish="2021-05-24T11:00:00")\nbarber.unset(start="2021-05-24T15:00:00", finish="2021-05-24T15:30:00")\n\n# Haircut takes 30 minutes\nprint(barber.get(minutes=30))\n\n```\n\nResult:\n\n```bash\n[\n    ["2021-05-24T10:00:00", "2021-05-24T10:30:00"],\n    ["2021-05-24T11:00:00", "2021-05-24T11:30:00"],\n    ["2021-05-24T11:30:00", "2021-05-24T12:00:00"],\n    ["2021-05-24T12:00:00", "2021-05-24T12:30:00"],\n    ["2021-05-24T12:30:00", "2021-05-24T13:00:00"],\n    ["2021-05-24T13:00:00", "2021-05-24T13:30:00"],\n    ["2021-05-24T13:30:00", "2021-05-24T14:00:00"],\n    ["2021-05-24T14:00:00", "2021-05-24T14:30:00"],\n    ["2021-05-24T14:30:00", "2021-05-24T15:00:00"],\n    ["2021-05-24T15:30:00", "2021-05-24T16:00:00"],\n]\n```\n\nTo use the development environment:\n\n    make dev\n\n## Releasing\n\n    poetry version major | minor | patch\n    make release\n',
    'author': 'Lewis',
    'author_email': 'lewis@fruiti.app',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fruiti-ltd/secondstate',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
