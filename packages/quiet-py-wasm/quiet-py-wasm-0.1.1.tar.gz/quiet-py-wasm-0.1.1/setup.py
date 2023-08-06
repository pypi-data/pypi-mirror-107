# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['quiet_py_wasm']

package_data = \
{'': ['*']}

install_requires = \
['PyAudio>=0.2.11,<0.3.0',
 'wasmer-compiler-cranelift==1.0.0',
 'wasmer>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'quiet-py-wasm',
    'version': '0.1.1',
    'description': 'Python interface to WASM build of Quiet. Work in progress: Current not suitable for use.',
    'long_description': None,
    'author': 'Martin Moxon',
    'author_email': 'moxon6@googlemail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
