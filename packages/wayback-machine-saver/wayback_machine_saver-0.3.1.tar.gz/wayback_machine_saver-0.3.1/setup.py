# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wayback_machine_saver']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'httpx>=0.18.0,<0.19.0', 'tqdm>=4.60.0,<5.0.0']

entry_points = \
{'console_scripts': ['wayback-machine-saver = '
                     'wayback_machine_saver.__main__:main']}

setup_kwargs = {
    'name': 'wayback-machine-saver',
    'version': '0.3.1',
    'description': 'Python tool for archiving web pages through Internet Archive Wayback Machine ',
    'long_description': '[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)\n[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg?style=flat-square)](https://conventionalcommits.org)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Github Actions](https://github.com/Lee-W/wayback-machine-saver/actions/workflows/python-check.yaml/badge.svg)](https://github.com/Lee-W/wayback-machine-saver/wayback-machine-saver/actions/workflows/python-check.yaml)\n[![PyPI Package latest release](https://img.shields.io/pypi/v/wayback_machine_saver.svg?style=flat-square)](https://pypi.org/project/wayback_machine_saver/)\n[![PyPI Package download count (per month)](https://img.shields.io/pypi/dm/wayback_machine_saver?style=flat-square)](https://pypi.org/project/wayback_machine_saver/)\n[![Supported versions](https://img.shields.io/pypi/pyversions/wayback_machine_saver.svg?style=flat-square)](https://pypi.org/project/wayback_machine_saver/)\n\n# Wayback Machine Saver\n\nPython tool for archiving web pages through Internet Archive Wayback Machine\n\n## Getting Started\n\n### Prerequisites\n* [Python](https://www.python.org/downloads/)\n* [pipx](https://pipxproject.github.io/pipx/installation/)\n\n\n## Installation\n\nIt\'s recommended to use tools like [pipx](https://pipxproject.github.io/pipx/installation/) to install this command-line tool.\n\n\n```sh\npipx install wayback-machine-saver\n```\n\n## Usage\n\n### Save pages\n\nSave URLs from the input file to [Internet Archive - Wayback Machine](http://web.archive.org/)\n\n```sh\nwayback_machine_saver save-pages FILENAME\n```\n\n#### Argument\n* FILENAME: filename to the file that consists of URLs to save\n\ne.g.,\n\n```txt\nhttps://example.com\nhttps://another-example.com\n```\n\n#### options\n\n*  --deliminator TEXT         [default:  "\\n"]\n*  --error-log-filename TEXT  [default: save-pages-error-log-"timestamp".csv]\n\n## Get latest archive urls\nAfter the URLs have been saved, [Internet Archive - Wayback Machine](http://web.archive.org/) will snap-shot the page to their database and create a timestamp. You can access the latest one through `http://web.archive.org/web/[Your URL]` and it will be redirected to `http://web.archive.org/web/[timestamp]/[Your URL]`. This command is used to get the redirected URLs.\n\n```sh\nwayback_machine_saver get-latest-archive-urls FILENAME\n```\n\n#### Argument\n* FILENAME: filename to the file that consists of URLs to retrieved\n\ne.g.,\n\n```txt\nhttps://example.com\nhttps://another-example.com\n```\n\n#### options\n\n*  --deliminator TEXT         [default: "\\n"]\n*  --output-filename TEXT     [default: retrieved-urls-"timestamp".csv]]\n*  --error-log-filename TEXT  [default: get-url-error-log-"timestamp".csv]\n\n## Configuration\n\nWayback Machine Saves supports configurating through environment variable. You can run `export VARIABLE=VALUE` before running the script to change the behavior.\n\n* WAYBACK_MACHINE_SAVER_RETRY_TIMES\n    * times to retry (default: 3)\n* HTTPX_TIMEOUT\n    * timeout for all GET operations (default: 10)\n\n## Contributing\nSee [Contributing](contributing.md)\n\n## Authors\nWei Lee <weilee.rx@gmail.com>\n\nCreated from [Lee-W/cookiecutter-python-template](https://github.com/Lee-W/cookiecutter-python-template/tree/0.9.0) version 0.9.0\n',
    'author': 'Wei Lee',
    'author_email': 'weilee.rx@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Lee-W/wayback-machine-saver',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
