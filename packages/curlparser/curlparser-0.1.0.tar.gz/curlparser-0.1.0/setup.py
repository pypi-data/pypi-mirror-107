# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['curlparser']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'curlparser',
    'version': '0.1.0',
    'description': 'Parse cURL commands returning object representing the request.',
    'long_description': '# cURL Parser\n\nParse cURL commands returning object representing the request.\n\n## How to install?\n\n`curlparser` is available on PyPi:\n\n### Using pip\n\n```shell\n$ pip install curlparser\n```\n### Using poetry\n\n```shell\n$ poetry add curlparser\n```\n\n### Using pipenv\n\n```shell\n$ pipenv install curlparser\n```\n\n## How to use?\n\n```python\n>>> import curlparser\n\n>>> result = curlparser.parse(\n    """\n    curl \\\n      --header \'Content-Type: application/json\' \\\n      --request PUT \\\n      --user nlecoy:my_password \\\n      --data \'{"username":"xyz", "password":"xyz"}\' \\\n      https://api.github.com/repos/nlecoy/curlparser\n    """\n)\n\n>>> result.url\n\'https://api.github.com/repos/nlecoy/curlparser\'\n\n>>> result.auth\n(\'nlecoy\', \'my_password\')\n\n>>> result.json\n{\'username\': \'xyz\', \'password\': \'xyz\'}\n```\n\n## Available parameters\n\n`curlparser`\'s parse method will return a `ParsedCommand` object containing the following fields:\n\n- method\n- url\n- auth\n- cookies\n- data\n- json\n- header\n- verify\n\n## License\n\ncURL Parser is distributed under the Apache 2.0. See [LICENSE](LICENSE) for more information.\n',
    'author': 'Nicolas Lecoy',
    'author_email': 'nicolas.lecoy@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nlecoy/curlparser',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
