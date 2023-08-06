# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['bgraph', 'bgraph.builder', 'bgraph.parsers', 'bgraph.viewer']

package_data = \
{'': ['*']}

install_requires = \
['networkx>=2.5,<3.0',
 'pydot>=1.4.2,<2.0.0',
 'pyparsing>=2.4.7,<3.0.0',
 'rich>=9.11.0,<10.0.0',
 'sh>=1.14.1,<2.0.0',
 'typer[all]>=0.3.2,<0.4.0',
 'untangle>=1.1.1,<2.0.0']

extras_require = \
{'doc': ['mkdocs>=1.1.2,<2.0.0',
         'mkdocs-material>=7.1.3,<8.0.0',
         'mkdocstrings>=0.15.0,<0.16.0']}

entry_points = \
{'console_scripts': ['bgraph = bgraph.main:app']}

setup_kwargs = {
    'name': 'bgraph',
    'version': '0.1.0',
    'description': '',
    'long_description': "BGraph\n======\n\n`BGraph` is a tool designed to generate dependencies graphs from `Android.bp` soong files.\n\n## Overview\n`BGraph` (for `Build-Graphs`) is a project aimed at create build graphs from _blueprints_ in AOSP and querying those graphs.\n\nIn short, this project builds/uses Unified Dependency Graph for the [Android Open Source Project](https://source.android.com/) by parsing and linking modules \ndefined in the Android build system [Soong](https://source.android.com/setup/build). \n\n### Use-cases\n\nYou should use this tool if you want to find:\n\n* all the dependencies of a source file in AOSP; \n* all the sources involved in the building of a target in AOSP;\n* common dependencies between two targets.\n\n\n## Usage\n```bash\n% bgraph --help                                                       \nUsage: bgraph [OPTIONS] COMMAND [ARGS]...\n\n  BGraph - generate and query build dependency graphes.\n\n  BGraph is used to manipulate build dependency graphs generated from\n  blueprint files. The main commands are:\n\n      - generate : used to generates multiples graphs\n\n      - query: used to query a previously generated graph\n\n  To get more help, see the online documentation.\n\nOptions:\n  -v, --verbose         Activate verbose output  [default: False]\n  --install-completion  Install completion for the current shell.\n  --show-completion     Show completion for the current shell, to copy it or\n                        customize the installation.\n\n  --help                Show this message and exit.\n\nCommands:\n  generate         Generate BGraph's from a mirror dir.\n  generate-single  Generate a BGraph from a branch.\n  list             List the BGraph already generated.\n  query            Query a BGraph.\n```\n\n## Installation\n\n### Using poetry\n```bash\npoetry install bgraph\n```\n\n### Using pip\n```bash\npip install bgraph\n```\n\n### Using docker\n```bash\ndocker build -f docker/Dockerfile -t bgraph .\n```\n\nThis will create a container with `git`, `repo` and `bgraph` and will take some time (because it compiles git from the source).\n\nSee [Docker](docs/docker.md) for more instructions.\n\n## Prerequisites\n- python3.8\n  \n### Optional dependencies for the builder:\n- repo\n- git (>25): since we're using partial-checkouts, a modern version of git is required\n- at least **1Go** of free disk space\n- (Optional: AOSP mirror)\n\nSee [Building from AOSP](docs/building.md) for more details.\n\n## Documentation\n[Documentation](https://achallande.doc.qb/bgraph)\n\n## Licence\n[Apache-2](https://choosealicense.com/licenses/apache-2.0)\n\n## Contributing\nContributions are always welcome!\n\nSee the [Contribution](docs/contribute.md) documentation for details on all you need to know about contributing.\n\n\n## Authors\n- dm (achallande@quarkslab.com)\n",
    'author': 'A. Challande',
    'author_email': 'achallande@quarkslab.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
