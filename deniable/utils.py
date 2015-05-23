# -*- coding: utf-8 -*-
import base64
from Crypto import Random
from Crypto.PublicKey.ElGamal import ElGamalobj
from Crypto.Util import Counter, number

__author__ = 'shunghsiyu'


def export_elgamal_key(key):
    assert isinstance(key, ElGamalobj)
    if hasattr(key, 'x'):
        key_info = (key.p, key.g, key.y, key.x)
    else:
        key_info = (key.p, key.g, key.y)
    return '\n'.join(str(n) for n in key_info)


def is_equal(a, b):
    # Mitigate timing attack
    # from: http://codahale.com/a-lesson-in-timing-attacks/

    if len(a) != len(b):
        return False

    result = 0
    for x, y in zip(a, b):
        result |= ord(x) ^ ord(y)

    return result == 0


class Deniable(object):
    def __init__(self, identity):
        self._identity = unicode(identity).encode('utf-8')
        self._n = 32

    def _iv(self):
        return number.bytes_to_long(Random.get_random_bytes(self._n))

    def _ctr(self, iv=None):
        if iv is None:
            iv = self._iv()
        return Counter.new(128, initial_value=iv)

    def enc(self, data, recipient):
        return self._enc(data, recipient)

    def enc_base64(self, data, recipient):
        return base64.b64encode(self._enc(data, recipient))

    def dec(self, payload_serialized):
        return self._dec(payload_serialized)

    def dec_base64(self, payload_serialized):
        return self._dec(base64.b64decode(payload_serialized))

    def publickey(self, target):
        return self._publickey(target)

    def privatekey(self):
        return self._privatekey()

