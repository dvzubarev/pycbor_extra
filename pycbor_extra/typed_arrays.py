#!/usr/bin/env python
# coding: utf-8

import logging
import array

from pycbor_extra.base_arrays import _BaseEnc, ARRAY_TAGS


try:
    import numpy as np
    _numpy_avail = True

    from pycbor_extra.numpy_arrays import NumpyEnc

except ImportError:
    _numpy_avail = False
    np = None

_logger = logging.getLogger("PyCborExtra")

class PyArrEnc(_BaseEnc):
    def __init__(self):
        int_typecodes = ['B', 'H', 'L', 'Q']
        float_typecodes = [None, 'f', 'd', None]
        super().__init__(int_typecodes, float_typecodes)

    def create_cbor_tag(self, obj):
        return self._create_cbor_tag(obj, obj.typecode)

    def create_obj_from_tag(self, tag):
        return self._create_obj_from_tag(tag, array.array)

PY_ARR_ENC = None
NUMPY_ENC = None


def _get_typed_arr_enc():
    global NUMPY_ENC
    global PY_ARR_ENC

    if _numpy_avail:
        if NUMPY_ENC is None:
            NUMPY_ENC = NumpyEnc()
            _logger.info("Numpy support is enabled since numpy is installed.")
        return NUMPY_ENC
    raise RuntimeError("PyCborExtra: numpy is not installed!")
    #TODO is array compat?
    #It might be akward if client does not have numpy installed and tries to decode ndarrays with array.array
    # if PY_ARR_ENC is None:
    #     PY_ARR_ENC = PyArrEnc()
    # return PY_ARR_ENC


def arr_hook(decoder, tag):
    global PY_ARR_ENC

    if tag.tag in ARRAY_TAGS:
        if PY_ARR_ENC is None:
            PY_ARR_ENC = PyArrEnc()
        return PY_ARR_ENC.create_obj_from_tag(tag)
    return tag

def default_hook(decoder, tag):
    if tag.tag in ARRAY_TAGS:
        enc = _get_typed_arr_enc()
        return enc.create_obj_from_tag(tag)
    return tag


def arr_default(encoder, obj):
    global PY_ARR_ENC

    if isinstance(obj, array.array):
        if PY_ARR_ENC is None:
            PY_ARR_ENC = PyArrEnc()
        encoder.encode(PY_ARR_ENC.create_cbor_tag(obj))
        return True
    return False

def default(encoder, obj):
    # if isinstance(obj, array.array):
    #     encoder.encode(PY_ARR_ENC.create_cbor_tag(obj))
    if _numpy_avail and isinstance(obj, np.ndarray):
        enc = _get_typed_arr_enc()
        encoder.encode(enc.create_cbor_tag(obj))
        return True
    return False
