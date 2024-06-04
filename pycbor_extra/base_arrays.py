#!/usr/bin/env python

import sys

import cbor2


def is_float(tag):
    return tag >> 4 & 1


def is_signed(tag):
    return tag >> 3 & 1


def is_le(tag):
    return tag >> 2 & 1


def needs_swap(tag):
    length = tag & 0b11
    if is_float(tag) == 0 and length == 0:
        return False
    if sys.byteorder == 'big':
        return is_le(tag)
    return not is_le(tag)


ARRAY_TAGS = range(64, 88)


class _BaseEnc:
    def __init__(self, int_typecodes, float_typecodes):
        self._int_typecodes = int_typecodes
        self._sint_typecodes = [n.lower() for n in int_typecodes]
        self._float_typecodes = float_typecodes

        self._encode_map = self._create_encode_map()

    def _tag_to_type(self, tag):
        length = tag & 0b11
        if is_float(tag):
            return self._float_typecodes[length]
        if is_signed(tag):
            return self._sint_typecodes[length]
        return self._int_typecodes[length]

    def _create_encode_map(self):
        encode_map = {}
        for tag in ARRAY_TAGS:
            if needs_swap(tag):
                continue
            typecode = self._tag_to_type(tag)
            if typecode is None:
                continue
            if typecode not in encode_map:
                encode_map[typecode] = tag
        return encode_map

    def _create_cbor_tag(self, obj, typecode):
        tag = self._encode_map[typecode]
        return cbor2.CBORTag(tag, obj.tobytes())

    def _create_obj_from_tag(self, tag, initer):
        dtype = self._tag_to_type(tag.tag)
        if dtype is None:
            return tag
        value = initer(dtype, tag.value)
        if needs_swap(tag.tag):
            value.byteswap()
        return value
