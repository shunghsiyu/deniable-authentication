#!/usr/bin/python
# -*- coding: utf-8 -*-
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Hash import HMAC, SHA256
from Crypto.PublicKey import ElGamal
from original import Original

__author__ = 'shunghsiyu'


class DiffieHellman(Original):
    def __init__(self, identity):
        super(DiffieHellman, self).__init__(identity)
        self._n = 16

    def enc(self, data, A, B):

        N = Random.get_random_bytes(self._n)
        kAB = ''

        ksess = HMAC.new(kAB, '0'+N, SHA256).digest()
        ksess2 = HMAC.new(kAB, '1'+N, SHA256).digest()

        aes = AES.new(ksess, AES.MODE_CTR, counter=self._ctr())
        ABdata = (A, B, data)
        C = aes.encrypt(ABdata)

        M = HMAC.new(ksess2, C+N, SHA256).digest()

        payload = (C, N, M)
        return payload

    def dec(self, payload_serialized):
        raise NotImplementedError()

    def publickey(self, target):
        with open(target+'.pub', 'r') as f:
            publickey = ElGamal.construct(f.read().splitlines())
        return publickey

    def privatekey(self):
        with open(self._identity, 'r') as f:
            privatekey = ElGamal.construct(f.read().splitlines())
        assert privatekey.has_private()
        return privatekey