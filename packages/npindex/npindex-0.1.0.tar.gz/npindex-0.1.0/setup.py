# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['npindex']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'npindex',
    'version': '0.1.0',
    'description': 'Provide an intuitive way to make ndarray indexing variable.',
    'long_description': '*******\nSummary\n*******\n\nProvide an intuitive way to make ndarray indexing variable like this::\n\n    from npindex import npidx\n\n    green_idx = npidx[:, :, 1]\n    green_of_im1 = im1[green_idx]\n    green_of_im2 = im2[green_idx]\n\nThis is all ``npindex`` does.\n\n*******\nInstall\n*******\nLinux, Windows, macOS::\n\n    pip install npindex\n\n',
    'author': 'kenjimaru',
    'author_email': 'kendimaru2@gmail.com',
    'maintainer': 'kenjimaru',
    'maintainer_email': 'kendimaru2@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
