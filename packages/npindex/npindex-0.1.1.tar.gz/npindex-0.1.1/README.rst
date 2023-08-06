*******
Summary
*******

Provide an intuitive way to make ndarray indexing variable like this::

    from npindex import npidx

    green_idx = npidx[:, :, 1]

    # assume that im1 and im2 are numpy ndarray
    # that were return values of OpenCV's cv2.imread() function.
    green_of_im1 = im1[green_idx]
    green_of_im2 = im2[green_idx]

This is all ``npindex`` does.

*****
Usage
*****

==============================
The signagure of npindex.npidx
==============================
::

    npidx(d1, d2=None, d3=None, /)

Only positional argument is permitted. And 1, 2, 3 dimentional ndarrays are only supported.

Each arguments are treated as a slice object when arguments are passed in the form of slicing notation::

    npidx[1:2, 3:4, 5:6]
    # => (slice(1, 2, None), slice(3, 4, None), slice(5, 6, None))

Or, treated as an integer when arguments are passed just as an integer::

    npidx[1, 2, 3] # => (1, 2, 3)

What is the point of that?
OK, I'll show you it in the next section.

======================
How to use effectively
======================

We can access to items of ndarray by passing one or more slice objects inside its square brackets like this::

    import numpy as np
    from npindex import npidx

    a = np.arange(10) # a => array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    i = npidx[1:5] # i => slice(1, 5, None)
    a[i] # => array([1, 2, 3, 4])

    a2 = a.reshape(2, 5) # a => array([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]])
    i2 = npidx[:, 2:4] # i2 => (slice(None, None, None), slice(2, 4, None))
    a2[i2] # => array([[2, 3], [7, 8]])

And it is also possible to access just one value from ndarray::

    import numpy as np
    from npindex import npidx

    a = np.arange(10) # a => array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    i = npidx[1] # i => 1
    a[i] # => 1

    a2 = a.reshape(2, 5) # a => array([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]])
    i2 = npidx[0, 4] # (0, 4)
    a2[i2] # => 4

When we want to access values from two or more ndarray object, npidx is useful.::

    import numpy as np
    from npindex import npidx

    range = npidx[100:300, 150:250, :]
    small_im1 = im1[range]
    small_im2 = im2[range]



*******
Install
*******
Linux, Windows, macOS::

    pip install npindex

