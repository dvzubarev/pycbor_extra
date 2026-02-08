#!/usr/bin/env python

import cbor2

import pycbor_extra.extra_tags as et

def test_excep():
    excep = Exception("Unk Error!")

    b = cbor2.dumps(excep, default=et.default)
    excep2 = cbor2.loads(b, tag_hook=et.default_hook)

    assert str(excep) == str(excep2)
