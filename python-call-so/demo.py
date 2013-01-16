#!/usr/bin/env python

import ctypes

lib_handle = ctypes.CDLL('libtest.so')
print lib_handle.sum(2, 4)

