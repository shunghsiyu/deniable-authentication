#!/usr/bin/python
# -*- coding: utf-8 -*-
from Finder.Containers_and_folders import container
from gen import containerxml
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Hash import HMAC, SHA256
from Crypto.PublicKey import ElGamal
from Crypto.Util import number
from original import Original
import pyxb

__author__ = 'shunghsiyu'


class DiffieHellman(Original):
    def __init__(self, identity):
        super(DiffieHellman, self).__init__(identity)
        self._n = 16

    def enc(self, data, A, B):

        N = Random.get_random_bytes(self._n)
        kAB_num = pow(self.publickey(B).y, self.privatekey().x, self.privatekey().p)
        kAB = number.long_to_bytes(kAB_num)
        ksess = HMAC.new(kAB, '\x00'+N, SHA256).digest()
        ksess2 = HMAC.new(kAB, '\x01'+N, SHA256).digest()

        aes = AES.new(ksess, AES.MODE_CTR, counter=self._ctr())
        ABdata_serialized = containerxml.container(pyxb.BIND(a=A, b=B, data=data)).toxml('utf-8')
        C = aes.encrypt(ABdata_serialized)

        CN_serialized = containerxml.container(pyxb.BIND(c=C, n=N)).toxml('utf-8')
        M = HMAC.new(ksess2, CN_serialized, SHA256).digest()

        payload = (C, N, M)
        return payload

    def dec(self, payload_serialized):
        C = payload_serialized[0]
        N = payload_serialized[1]
        M = payload_serialized[2]

        # TODO: get public key
        kAB_num = pow(self.privatekey().y, self.privatekey().x, self.privatekey().p)
        kAB = number.long_to_bytes(kAB_num)
        ksess = HMAC.new(kAB, '\x00'+N, SHA256).digest()
        ksess2 = HMAC.new(kAB, '\x01'+N, SHA256).digest()

        aes = AES.new(ksess, AES.MODE_CTR, counter=self._ctr())
        ABdata = containerxml.CreateFromDocument(aes.decrypt(C))
        A = ABdata.diffiehellman.a
        B = ABdata.diffiehellman.b
        data = ABdata.diffiehellman.data

        CN_serialized = containerxml.container(pyxb.BIND(c=C, n=N)).toxml('utf-8')
        M_calculated = HMAC.new(ksess2, CN_serialized, SHA256).digest()
        assert M == M_calculated

        return data

    def publickey(self, target):
        with open(target+'.pub', 'r') as f:
            publickey = ElGamal.construct(tuple(int(value) for value in f.read().splitlines()))
        return publickey

    def privatekey(self):
        with open(self._identity, 'r') as f:
            privatekey = ElGamal.construct(tuple(int(value) for value in f.read().splitlines()))
        assert privatekey.has_private()
        return privatekey