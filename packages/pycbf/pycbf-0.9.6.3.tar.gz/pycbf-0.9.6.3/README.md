# `pycbf` - CBFlib for python

[![PyPI release](https://img.shields.io/pypi/v/pycbf.svg)](https://pypi.python.org/pypi/pycbf)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/pycbf.svg)](https://pypi.org/project/pycbf)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)]( https://github.com/ambv/black)
        
This repository builds the `pycbf` portion of [CBFlib] only, as a [manylinux]
binary wheel installable through `pip install pycbf`.

In order to do this, it has some limitations compared to the full build of CBFlib:

-   No HDF5 bindings
-   No (custom) libTiff bindings
-   No CBF regex capabilities
-   No header files included - this is not intended to be used as a linking
    target

In addition to the base 0.9.6, this has the following alterations:

| Version     | Changes                                                                                             |
| ----------- | --------------------------------------------------------------------------------------------------- |
| 0.9.6.0     | Regenerated SWIG bindings for Python 3 compatibility. Compiled with `SWIG_PYTHON_STRICT_BYTE_CHAR`. |
| ~~0.9.6.1~~ | This was an unreleased internal version.                                                            |
| 0.9.6.2     | Drop python 2.7. Accept both `bytes` and `str`. Add `read_buffer` method, and `libimg` bindings.    |
| 0.9.6.3     | Clean up the package installation to remove source-only files.                                      |

For details, please see the [CHANGELOG](CHANGELOG.rst).

[cbflib]: https://github.com/yayahjb/cbflib
[manylinux]: https://www.python.org/dev/peps/pep-0571/
[`yayahjb/cbflib#19`]: https://github.com/yayahjb/cbflib/pull/19
