pyfastcopy
==========

[![Latest Version](https://img.shields.io/pypi/v/pyfastcopy.svg?style=flat)](https://pypi.python.org/pypi/pyfastcopy/)
[![Tests Status](https://img.shields.io/travis/desbma/pyfastcopy/master.svg?label=tests&style=flat)](https://travis-ci.org/desbma/pyfastcopy)
[![Coverage](https://img.shields.io/coveralls/desbma/pyfastcopy/master.svg?style=flat)](https://coveralls.io/r/desbma/pyfastcopy?branch=master)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/pyfastcopy.svg?style=flat)](https://pypi.python.org/pypi/pyfastcopy/)
[![License](https://img.shields.io/github/license/desbma/pyfastcopy.svg?style=flat)](https://pypi.python.org/pypi/pyfastcopy/)

pyfastcopy is a simple Python module that monkey patches the `shutil.copyfile` function of Python standard library to internally use the sendfile system call.

It can provide important performance improvements for large file copy (typically 30-40%). See [the performance section](#Performance) for some numbers.

Because `shutil.copyfile` is used by other fonctions in the `shutil` module, the following functions also automatically benefit from the performance boost:

* `shutil.copy`
* `shutil.copy2`
* `shutil.copytree`

If sendfile is not available on your system or fails, the classic, slower chunk file copy is used, so there is no downside to using this module.

For more information, see [my proposed patch](https://bugs.python.org/issue25156) for Python.


## Performance

Tests were done copying files (source and destination) on a [tmpfs](https://en.wikipedia.org/wiki/Tmpfs) filesystem, so that no slowdown related to hard drive or SSD storage occurs. Test files were generated with pseudo random data using [frandom](http://www.billauer.co.il/frandom.html).

See [benchmark.py](https://github.com/desbma/pyfastcopy/blob/master/benchmark.py) for details about the test procedure and how the following graphs were generated.

[![Imgur](http://i.imgur.com/0TZTs4Oh.png)](http://i.imgur.com/0TZTs4O.png)

[![Imgur](http://i.imgur.com/op8HxaCh.png)](http://i.imgur.com/op8HxaC.png)

These tests show a 30-40% performance gain compared to stock Python shutil.copy:

[![Imgur](http://i.imgur.com/V4dIgSyh.png)](http://i.imgur.com/V4dIgSy.png)


## Usage

Just import the module:

    import pyfastcopy

And then use the patched shutil.copyfile as usual:

    shutil.copyfile(src, dst)

**The `sendfile` system call does not exist on Windows, so importing this module will have no effect.**


## Installation

### From PyPI (with PIP)

1. If you don't already have it, [install pip](http://www.pip-installer.org/en/latest/installing.html) for Python 3 (not needed if you are using Python >= 3.4)
2. Install pyfastcopy: `pip3 install pyfastcopy`
3. Enjoy fast fast copy when using `shutil.copyfile`, `shutil.copy`, `shutil.copy2` or `shutil.copytree`

### From source

1. If you don't already have it, [install setuptools](https://pypi.python.org/pypi/setuptools#installation-instructions) for Python 3
2. Clone this repository: `git clone https://github.com/desbma/pyfastcopy`
3. Install pyfastcopy: `python3 setup.py install`
4. Enjoy fast fast copy when using `shutil.copyfile`, `shutil.copy`, `shutil.copy2` or `shutil.copytree`


## License

Python Software Foundation License
