#!/usr/bin/env python

import cbor2

PYEXCEP_TAG = 79500

def default_hook(decoder, tag):
    if tag.tag == PYEXCEP_TAG:
        return Exception(tag.value)
    return tag


def default(encoder, obj):
    if isinstance(obj, Exception):
        #Keep it simple for now
        encoder.encode(cbor2.CBORTag(PYEXCEP_TAG, str(obj)))
        return True
    return False
