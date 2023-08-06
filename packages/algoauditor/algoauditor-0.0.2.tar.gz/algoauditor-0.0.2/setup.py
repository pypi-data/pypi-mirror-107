# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['algoauditor', 'algoauditor.utils']

package_data = \
{'': ['*'], 'algoauditor': ['public/*']}

install_requires = \
['numpy>=1.19.4,<2.0.0', 'requests>=2.25.0,<3.0.0']

setup_kwargs = {
    'name': 'algoauditor',
    'version': '0.0.2',
    'description': 'Lethical AI Python Library with cloud support',
    'long_description': '# Lethai Library\nThe library, named "lethai", provides a standard library to interact with the services provided by Lethical.ai.\n\n\n## Getting Started\n\n### Generate API Key\nSteps to follow\n\n  - Create an account on Lethical.ai\n  - Click on API Keys on the side panel\n  - Click "add key" button\n    - Provide tags to the key if needed (They will help you identify and filter the keys for your reference)\n    - Choose the access level for the key\n    - Click on generate\n  - A key will be displayed on the screen please copy it and store it safely for future usage.\n\n*NOTE: The key will only be shown once. This is for security purposes*\n\n### Installation\n> pip3 install lethai\n\n### Usage\nThe various features provided by our library include the following:\n\n- Discrimination detection\n  -[NLG models](./docs/discrimination.md)\n',
    'author': 'Amanl04',
    'author_email': 'amanlodha423@outlook.com',
    'maintainer': 'Aman Lodha',
    'maintainer_email': 'aman@lethical.ai',
    'url': 'https://lethical.ai',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
