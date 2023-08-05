# cython: language_level=2
import numpy as np
cimport numpy as np
cimport cython
from libc.math cimport exp, cos, sin, pi, pow, sqrt, erfc
from cython.parallel import prange


out_shape = {}
coordination = {}
resolving = {}


$kernels