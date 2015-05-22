#!/usr/bin/python
# -*- coding: utf-8 -*-
from Crypto.PublicKey.ElGamal import ElGamalobj

__author__ = 'shunghsiyu'


def export_elgamal_key(key):
    assert isinstance(key, ElGamalobj)
    if hasattr(key, 'x'):
        key_info = (key.p, key.g, key.y, key.x)
    else:
        key_info = (key.p, key.g, key.y)
    return '\n'.join(str(n) for n in key_info)