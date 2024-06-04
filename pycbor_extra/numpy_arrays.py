#!/usr/bin/env python

import numpy as np

from pycbor_extra.base_arrays import _BaseEnc


class NumpyEnc(_BaseEnc):
    def __init__(self):
        int_typecodes = ['B', 'H', 'I', 'L']
        float_typecodes = ['e', 'f', 'd', 'g']
        super().__init__(int_typecodes, float_typecodes)

    def create_cbor_tag(self, obj):
        return self._create_cbor_tag(obj, obj.dtype.char)

    def create_obj_from_tag(self, tag):
        return self._create_obj_from_tag(tag, lambda c, b: np.frombuffer(b, dtype=np.dtype(c)))
