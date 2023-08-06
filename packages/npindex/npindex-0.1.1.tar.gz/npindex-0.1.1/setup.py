# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['npindex']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'npindex',
    'version': '0.1.1',
    'description': 'Provide an intuitive way to make ndarray indexing variable.',
    'long_description': "*******\nSummary\n*******\n\nProvide an intuitive way to make ndarray indexing variable like this::\n\n    from npindex import npidx\n\n    green_idx = npidx[:, :, 1]\n\n    # assume that im1 and im2 are numpy ndarray\n    # that were return values of OpenCV's cv2.imread() function.\n    green_of_im1 = im1[green_idx]\n    green_of_im2 = im2[green_idx]\n\nThis is all ``npindex`` does.\n\n*****\nUsage\n*****\n\n==============================\nThe signagure of npindex.npidx\n==============================\n::\n\n    npidx(d1, d2=None, d3=None, /)\n\nOnly positional argument is permitted. And 1, 2, 3 dimentional ndarrays are only supported.\n\nEach arguments are treated as a slice object when arguments are passed in the form of slicing notation::\n\n    npidx[1:2, 3:4, 5:6]\n    # => (slice(1, 2, None), slice(3, 4, None), slice(5, 6, None))\n\nOr, treated as an integer when arguments are passed just as an integer::\n\n    npidx[1, 2, 3] # => (1, 2, 3)\n\nWhat is the point of that?\nOK, I'll show you it in the next section.\n\n======================\nHow to use effectively\n======================\n\nWe can access to items of ndarray by passing one or more slice objects inside its square brackets like this::\n\n    import numpy as np\n    from npindex import npidx\n\n    a = np.arange(10) # a => array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])\n    i = npidx[1:5] # i => slice(1, 5, None)\n    a[i] # => array([1, 2, 3, 4])\n\n    a2 = a.reshape(2, 5) # a => array([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]])\n    i2 = npidx[:, 2:4] # i2 => (slice(None, None, None), slice(2, 4, None))\n    a2[i2] # => array([[2, 3], [7, 8]])\n\nAnd it is also possible to access just one value from ndarray::\n\n    import numpy as np\n    from npindex import npidx\n\n    a = np.arange(10) # a => array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])\n    i = npidx[1] # i => 1\n    a[i] # => 1\n\n    a2 = a.reshape(2, 5) # a => array([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]])\n    i2 = npidx[0, 4] # (0, 4)\n    a2[i2] # => 4\n\nWhen we want to access values from two or more ndarray object, npidx is useful.::\n\n    import numpy as np\n    from npindex import npidx\n\n    range = npidx[100:300, 150:250, :]\n    small_im1 = im1[range]\n    small_im2 = im2[range]\n\n\n\n*******\nInstall\n*******\nLinux, Windows, macOS::\n\n    pip install npindex\n\n",
    'author': 'kenjimaru',
    'author_email': 'kendimaru2@gmail.com',
    'maintainer': 'kenjimaru',
    'maintainer_email': 'kendimaru2@gmail.com',
    'url': 'https://github.com/kendimaru/npindex',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
