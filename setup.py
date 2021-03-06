#!/usr/bin/env python
import os
import sys
from glob import glob
from distutils.core import setup
from distutils.extension import Extension
from distutils.dist import Distribution
import re


if os.path.exists("sep.pyx"):
    USE_CYTHON = True
    fname = "sep.pyx"
else:
    USE_CYTHON = False
    fname = "sep.c"

if (any('--' + opt in sys.argv for opt in Distribution.display_option_names +
        ['help-commands', 'help']) or len(sys.argv) == 1
    or sys.argv[1] in ('egg_info', 'clean', 'help')):
    extensions=[]
else:
    try:
        import numpy
    except ImportError:
        raise SystemExit("NumPy is required for '{}'".format(sys.argv[1]))

    sourcefiles = [fname] + glob(os.path.join("src", "*.c"))
    headerfiles = glob(os.path.join("src", "*.h"))
    include_dirs=[numpy.get_include(), "src"]
    extensions = [Extension("sep", sourcefiles, include_dirs=include_dirs,
                            depends=headerfiles, extra_compile_args=['-g0'])]
    if USE_CYTHON:
        from Cython.Build import cythonize
        extensions = cythonize(extensions)

# Synchronize version from code.
version = re.findall(r"__version__ = \"(.*?)\"", open(fname).read())[0]

description = "Astronomical source extraction and photometry library"
long_description = "http://sep.readthedocs.org"

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: GNU Lesser General Public License v3 "
    "or later (LGPLv3+)",
    "Topic :: Scientific/Engineering :: Astronomy",
    "Intended Audience :: Science/Research"]

setup(name="sep",
      version=version,
      description=description,
      long_description=long_description,
      license="LGPLv3+",
      classifiers=classifiers,
      url="https://github.com/kbarbary/sep",
      author="Kyle Barbary",
      author_email="kylebarbary@gmail.com",
      install_requires=['numpy'],
      ext_modules=extensions)
