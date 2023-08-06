# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2017 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################*/

__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "07/05/2021"


from est import settings
import silx.io.h5py_utils
import silx.io.utils
import os


@silx.io.h5py_utils.retry(retry_timeout=settings.DEFAULT_READ_TIMEOUT)
def get_data(url):
    """Returns a numpy data from an URL.

    Examples:

    >>> # 1st frame from an EDF using silx.io.open
    >>> data = silx.io.get_data("silx:/users/foo/image.edf::/scan_0/instrument/detector_0/data[0]")

    >>> # 1st frame from an EDF using fabio
    >>> data = silx.io.get_data("fabio:/users/foo/image.edf::[0]")

    Yet 2 schemes are supported by the function.

    - If `silx` scheme is used, the file is opened using
        :meth:`silx.io.open`
        and the data is reach using usually NeXus paths.
    - If `fabio` scheme is used, the file is opened using :meth:`fabio.open`
        from the FabIO library.
        No data path have to be specified, but each frames can be accessed
        using the data slicing.
        This shortcut of :meth:`silx.io.open` allow to have a faster access to
        the data.

    .. seealso:: :class:`silx.io.url.DataUrl`

    :param Union[str,silx.io.url.DataUrl]: A data URL
    :rtype: Union[numpy.ndarray, numpy.generic]
    :raises ImportError: If the mandatory library to read the file is not
        available.
    :raises ValueError: If the URL is not valid or do not match the data
    :raises IOError: If the file is not found or in case of internal error of
        :meth:`fabio.open` or :meth:`silx.io.open`. In this last case more
        informations are displayed in debug mode.
    """
    if not isinstance(url, silx.io.url.DataUrl):
        url = silx.io.url.DataUrl(url)

    if not url.is_valid():
        raise ValueError("URL '%s' is not valid" % url.path())

    if not os.path.exists(url.file_path()):
        raise IOError("File '%s' not found" % url.file_path())

    if url.scheme() == "silx":
        data_path = url.data_path()
        data_slice = url.data_slice()

        with silx.io.h5py_utils.File(url.file_path(), "r") as h5:
            if data_path not in h5:
                raise ValueError("Data path from URL '%s' not found" % url.path())
            data = h5[data_path]

            if not silx.io.is_dataset(data):
                raise ValueError(
                    "Data path from URL '%s' is not a dataset" % url.path()
                )

            if data_slice is not None:
                data = silx.io.utils.h5py_read_dataset(data, index=data_slice)
            else:
                # works for scalar and array
                data = silx.io.utils.h5py_read_dataset(data)

    elif url.scheme() == "fabio":
        import fabio

        data_slice = url.data_slice()
        if data_slice is None:
            data_slice = (0,)
        if data_slice is None or len(data_slice) != 1:
            raise ValueError(
                "Fabio slice expect a single frame, but %s found" % data_slice
            )
        index = data_slice[0]
        if not isinstance(index, int):
            raise ValueError(
                "Fabio slice expect a single integer, but %s found" % data_slice
            )

        try:
            fabio_file = fabio.open(url.file_path())
        except Exception:
            raise IOError(
                "Error while opening %s with fabio (use debug for more information)"
                % url.path()
            )

        if fabio_file.nframes == 1:
            if index != 0:
                raise ValueError(
                    "Only a single frame available. Slice %s out of range" % index
                )
            data = fabio_file.data
        else:
            data = fabio_file.getframe(index).data

        # There is no explicit close
        fabio_file = None

    else:
        raise ValueError("Scheme '%s' not supported" % url.scheme())

    return data
