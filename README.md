[![PyPI version](https://img.shields.io/pypi/v/pyfastpfor.svg)](https://pypi.python.org/pypi/pyfastpfor/)
[![Downloads](https://pepy.tech/badge/pyfastpfor)](https://pepy.tech/project/pyfastpfor)
[![Build Status](https://travis-ci.org/searchivarius/PyFastPFor.svg?branch=master)](https://travis-ci.org/searchivarius/PyFastPFor)
# PyFastPFor
Python bindings for the fast **light-weight** integer compression library [FastPFor](https://github.com/lemire/FastPFor): A research library with integer compression schemes. FastPFor is broadly applicable to the compression of arrays of 32-bit integers where most integers are small. The library seeks to exploit SIMD instructions (SSE) whenever possible. This library can decode at least 4 billions of compressed integers per second on most desktop or laptop processors. That is, it can decompress data at a rate of 15 GB/s. This is significantly faster than generic codecs like gzip, LZO, Snappy or LZ4.

# Authors

Daniel Lemire, Leonid Boytsov, Owen Kaser, Maxime Caron, Louis Dionne, Michel Lemay, Erik Kruus, Andrea Bedini, Matthias Petri, Robson Braga Araujo, Patrick Damme. Bindings are created by Leonid Boytsov.

Setuptools/compiler changes for MacOS and ARM 64 by Jeff Ford.

# Installation

Bindings can be installed locally:
```
cd python_bindings
pip install -r requirements.txt
pip install .
```
or via pip from PyPi.org:
```
pip install pyfastpfor-osx-arm64
```



# Documentation

The library supports all the codecs implemented in the original [FastPFor](https://github.com/lemire/FastPFor) library by Feb 2018. To get a list of codecs, use the function ``getCodecList``.

Typical light-weight compression does not take context into account and, consequently, works well only for small integers. When integers are large, data differencing is a common trick to make integers small. In particular, we often deal with sorted lists of integers, which can be represented by differences between neighboring numbers.

The smallest differences (**fine** deltas) are between adjacent numbers. Respective differencing and difference inverting functions are ``delta1'' and ``prefixSum1''.

However, we can do reasonably well, we compute differences between numbers that are four positions apart (**coarse** deltas). Such differences can be computed and inverted more efficiently.  Respective differencing and difference inverting functions are ``delta4'' and ``prefixSum4''.

Examples of three common use scenarios (no differencing, coarse and fine deltas) are outlined in [this Python notebook](python_bindings/examples.ipynb).
