# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['grafeno',
 'grafeno.jupyter',
 'grafeno.linearizers',
 'grafeno.operations',
 'grafeno.transformers']

package_data = \
{'': ['*'],
 'grafeno.linearizers': ['simplenlg_lib/*'],
 'grafeno.transformers': ['freeling_conf/*']}

install_requires = \
['PyYAML', 'networkx>=2,<3', 'spacy>=2,<3']

extras_require = \
{'lexical': ['nltk'], 'modules': ['pexpect', 'numpy', 'scipy']}

entry_points = \
{'console_scripts': ['setup = grafeno.setup:setup']}

setup_kwargs = {
    'name': 'grafeno',
    'version': '0.3.0',
    'description': 'Concept graph library',
    'long_description': None,
    'author': 'Antonio F. G. Sevilla',
    'author_email': 'afgs@ucm.es',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
