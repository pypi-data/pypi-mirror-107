

class IndexGenerator:
    def __getitem__(self, d1, d2=None, d3=None, /):
        """
        Get slice object or array of slice objects that can be used to indexing ndarray.

        example::

            todo

        Parameters
        ----------
        d1: number or slice
        d2: number or slice
        d3: number or slice

        Returns
        -------
        slice or slice-list
            If only one parameter specified, return a slice object.
            Otherwise, return a list of slice objects.

        """
        print('__getitem__ called')

        if not d2:
            return d1
        elif not d3:
            return [d1, d2]
        else:
            return [d1, d2, d3]
