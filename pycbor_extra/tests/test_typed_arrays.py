#!/usr/bin/env python
# coding: utf-8

import array
import cbor2

import numpy as np

import pycbor_extra.typed_arrays as typed_arrays
import pycbor_extra.extra_tags as et


def test_python_array():
    arr = array.array('L', [1, 2, 3, 2 << 32])

    b = cbor2.dumps(arr, default=typed_arrays.arr_default)
    arr2 = cbor2.loads(b, tag_hook=typed_arrays.arr_hook)

    assert arr == arr2


def test_nested_python_array():
    arr = array.array('b', [0, 2, -64, 127])
    d = {'arr': arr, 's': 'str'}

    b = cbor2.dumps(d, default=typed_arrays.arr_default)
    d2 = cbor2.loads(b, tag_hook=typed_arrays.arr_hook)

    assert d == d2


def test_numpy_array():
    arr = np.arange(1, 5, dtype=np.uint32)
    b = cbor2.dumps(arr, default=et.default)
    arr2 = cbor2.loads(b, tag_hook=et.default_hook)
    np.testing.assert_array_equal(arr, arr2)


def test_numpy_array_fp16():
    arr = np.arange(1, 5, dtype=np.float16)
    b = cbor2.dumps(arr, default=et.default)
    arr2 = cbor2.loads(b, tag_hook=et.default_hook)
    np.testing.assert_array_equal(arr, arr2)


def test_ndarray():
    arr = np.random.rand(3, 10)
    b = cbor2.dumps(arr, default=et.default)
    arr2 = cbor2.loads(b, tag_hook=et.default_hook)
    arr2 = arr2.reshape(3, 10)
    np.testing.assert_array_equal(arr, arr2)
