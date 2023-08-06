*******
Summary
*******

Provide an intuitive way to make ndarray indexing variable like this::

    from npindex import npidx

    green_idx = npidx[:, :, 1]
    green_of_im1 = im1[green_idx]
    green_of_im2 = im2[green_idx]

This is all ``npindex`` does.

*******
Install
*******
Linux, Windows, macOS::

    pip install npindex

