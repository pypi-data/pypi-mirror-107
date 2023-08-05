# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['docrunner',
 'docrunner.constants',
 'docrunner.exceptions',
 'docrunner.languages',
 'docrunner.models',
 'docrunner.utils']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.8.1,<2.0.0', 'toml>=0.10.2,<0.11.0', 'typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['docrunner = docrunner.main:app']}

setup_kwargs = {
    'name': 'docrunner',
    'version': '0.1.7',
    'description': 'A command line tool which allows you to run the code in your markdown files to ensure that readers always have access to working code.',
    'long_description': "## Docrunner\n\nA command line tool which allows you to run the code in your markdown files to ensure that readers always have access to working code.\n\n## What does it do?\n\nDocrunner goes through your markdown file and runs any code in it, providing you safe testing for any markdown documentation. You can specify the path to the markdown file, along with other options, with flags.\n\n## Installation\n\nUse the package manager [pip](https://pip.pypa.io/en/stable/) to install docrunner.\n\n```powershell\npip install docrunner\n```\n\n## QuickStart\n\n```powershell\ndocrunner --help\n```\n\n### Language Specific Help\nFor help on a specific language, run:\n```powershell\ndocrunner <language> --help\n```\n\n### Python Example\n\n```powershell\ndocrunner python --markdown-path example/example.md --multi-file\n```\n\nThis command executes all python within `example.md` and does so by putting each snippet of python from this file into a separate file, and running each file. If you don't want each snippet in a separate python file, just remove the --multi-file option.\n\n\n## Contributing and Local Development\nPlease check the [CONTRIBUTING](/CONTRIBUTING.md) guidelines for information \non how to contribute to docrunner.\n\n## Supported Languages\n\n- Python - `docrunner python --help`\n- Javascript - `docrunner javascript --help`\n- Typescript - `docrunner typescript --help`\n- Dart - `docrunner dart --help`\n",
    'author': 'DudeBro249',
    'author_email': 'appdevdeploy@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DudeBro249/docrunner',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
