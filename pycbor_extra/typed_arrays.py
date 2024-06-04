#!/usr/bin/env python
# coding: utf-8

import logging
import array

import cbor2

from pycbor_extra.base_arrays import _BaseEnc, ARRAY_TAGS

try:
    import numpy as np

    from pycbor_extra.numpy_arrays import NumpyEnc

    NUMPY_ENC = NumpyEnc()

    logger = logging.getLogger("PyCborExtra")
    logger.info("Numpy support is enabled since numpy is installed.")


except ImportError:
    np = None
    NUMPY_ENC = None


class PyArrEnc(_BaseEnc):
    def __init__(self):
        int_typecodes = ['B', 'H', 'L', 'Q']
        float_typecodes = [None, 'f', 'd', None]
        super().__init__(int_typecodes, float_typecodes)

    def create_cbor_tag(self, obj):
        return self._create_cbor_tag(obj, obj.typecode)

    def create_obj_from_tag(self, tag):
        return self._create_obj_from_tag(tag, array.array)


PY_ARR_ENC = PyArrEnc()


def default(encoder, obj):
    if isinstance(obj, array.array):
        encoder.encode(PY_ARR_ENC.create_cbor_tag(obj))
    elif np is not None and NUMPY_ENC is not None and isinstance(obj, np.ndarray):
        encoder.encode(NUMPY_ENC.create_cbor_tag(obj))
    else:
        raise cbor2.CBOREncodeTypeError(f"cannot serialize type {type(obj)}")


def _hook(tag, enc):
    if tag.tag in ARRAY_TAGS:
        return enc.create_obj_from_tag(tag)
    return tag


def arr_hook(decoder, tag):
    return _hook(tag, PY_ARR_ENC)


def numpy_hook(decoder, tag):
    return _hook(tag, NUMPY_ENC)


def default_hook(decoder, tag):
    if NUMPY_ENC is not None:
        return numpy_hook(decoder, tag)
    return arr_hook(decoder, tag)
