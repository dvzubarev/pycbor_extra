import cbor2

from pycbor_extra.typed_arrays import default_hook as typed_arr_def_hook, default as typed_arr_def
from pycbor_extra.pyexceps import default_hook as excep_def_hook, default as excep_def


def default(encoder, obj):
    if typed_arr_def(encoder, obj):
        return
    if excep_def(encoder, obj):
        return
    raise cbor2.CBOREncodeTypeError(f"Cannot serialize type {type(obj)}")


def default_hook(decoder, tag):
    if (result := typed_arr_def_hook(decoder, tag)) is not tag:
        return result

    if (result := excep_def_hook(decoder, tag)) is not tag:
        return result

    return tag
