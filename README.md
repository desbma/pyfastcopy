pyfastcopy
==========

[![Latest version](https://img.shields.io/pypi/v/pyfastcopy.svg?style=flat)](https://pypi.python.org/pypi/pyfastcopy/)
[![Tests status](https://img.shields.io/travis/desbma/pyfastcopy/master.svg?label=tests&style=flat)](https://travis-ci.org/desbma/pyfastcopy)
[![Coverage](https://img.shields.io/coveralls/desbma/pyfastcopy/master.svg?style=flat)](https://coveralls.io/github/desbma/pyfastcopy?branch=master)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/pyfastcopy.svg?style=flat)](https://pypi.python.org/pypi/pyfastcopy/)

pyfastcopy is a simple Python module that monkey patches the `shutil.copyfile` function of Python standard library to internally use the sendfile system call.

It can provide important performance improvements for large file copy (typically 30-40%). See [the performance section](#performance) for some numbers.

Because `shutil.copyfile` is used by other fonctions in the `shutil` module, the following functions also automatically benefit from the performance boost:

* `shutil.copy`
* `shutil.copy2`
* `shutil.copytree`

If `sendfile` is not available on your system or fails, the classic, slower chunk file copy is used, so there is no downside to using this module.

For more information, see [my proposed patch](https://bugs.python.org/issue25156) for Python.


## Performance

Tests were done copying files (source and destination) on a [tmpfs](https://en.wikipedia.org/wiki/Tmpfs) filesystem, so that no slowdown related to hard drive or SSD storage occurs. Test files were generated with pseudo random data using [frandom](http://www.billauer.co.il/frandom.html).

See [benchmark.py](https://github.com/desbma/pyfastcopy/blob/master/benchmark.py) for details about the test procedure and how the following graphs were generated.

Python 3.4: [![graph1](https://i.imgur.com/fbKbKgmt.png)](https://i.imgur.com/fbKbKgm.png) [![graph2](https://i.imgur.com/Cnrwi2Yt.png)](https://i.imgur.com/Cnrwi2Y.png) [![graph3](https://i.imgur.com/B3GDWFrt.png)](https://i.imgur.com/B3GDWFr.png)

Python 3.6: [![graph4](https://i.imgur.com/5lnETSCt.png)](https://i.imgur.com/5lnETSC.png) [![graph5](https://i.imgur.com/YsBWYsxt.png)](https://i.imgur.com/YsBWYsx.png) [![graph6](https://i.imgur.com/k32LSbCt.png)](https://i.imgur.com/k32LSbC.png)

**These tests show a 30-50% performance improvement of `shutil.copyfile` compared to stock Python.**


## Usage

Just import the module:

    import pyfastcopy

And then use the patched `shutil.copyfile` as usual:

    shutil.copyfile(src, dst)

**The `sendfile` system call does not exist on Windows, so importing this module will have no effect.**


## Installation

### From PyPI (with PIP)

1. If you don't already have it, [install pip](https://pip.pypa.io/en/stable/installing/) for Python 3 (not needed if you are using Python >= 3.4)
2. Install pyfastcopy: `pip3 install pyfastcopy`
3. Enjoy fast copy when using `shutil.copyfile`, `shutil.copy`, `shutil.copy2` or `shutil.copytree`

### From source

1. If you don't already have it, [install setuptools](https://pypi.python.org/pypi/setuptools#installation-instructions) for Python 3
2. Clone this repository: `git clone https://github.com/desbma/pyfastcopy`
3. Install pyfastcopy: `python3 setup.py install`
4. Enjoy fast copy when using `shutil.copyfile`, `shutil.copy`, `shutil.copy2` or `shutil.copytree`


## License

Python Software Foundation License
