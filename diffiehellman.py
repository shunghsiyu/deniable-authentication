#!/usr/bin/python
# -*- coding: utf-8 -*-
from gen import containerxml, payloadxml
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Hash import HMAC, SHA256
from Crypto.PublicKey import ElGamal
from Crypto.Util import number
from Crypto.Random import random
from original import Original
import pyxb

__author__ = 'shunghsiyu'


class DiffieHellman(Original):
    def __init__(self, identity):
        super(DiffieHellman, self).__init__(identity)
        self._n = 16

    def enc(self, data, A, B):
        N = Random.get_random_bytes(self._n)
        mkAB_int = pow(self.publickey(B).y, self.privatekey().x, self.privatekey().p)
        mkAB = number.long_to_bytes(mkAB_int)
        skAB = HMAC.new(mkAB, N, SHA256).digest()

        K = random.randint(1+1, self.privatekey().p-1-1)
        ANdata_serialized = containerxml.container(pyxb.BIND(a=A, n=N, data=data)).toxml('utf-8')
        print(ANdata_serialized)
        t = Random.get_random_bytes(self._n)
        aest = AES.new(t, AES.MODE_CTR, counter=self._ctr())
        C = aest.encrypt(ANdata_serialized)

        P = self.publickey(B).encrypt(t, K)
        assert len(P) == 2
        M = HMAC.new(skAB, ''.join(P), SHA256).digest()

        payload_serialized = payloadxml.payload(pyxb.BIND(p1=P[0], p2=P[1], c=C, m=M)).toxml('utf-8')
        return payload_serialized

    def dec(self, payload_serialized):
        payload = payloadxml.CreateFromDocument(payload_serialized)
        P1 = str(payload.diffiehellman.p1)
        P2 = str(payload.diffiehellman.p2)
        P = (P1, P2)
        C = payload.diffiehellman.c
        M = payload.diffiehellman.m

        t = self.privatekey().decrypt(P)
        aest = AES.new(t, AES.MODE_CTR, counter=self._ctr())
        ANdata_serialized = aest.decrypt(C)
        print(ANdata_serialized)
        ANdata = containerxml.CreateFromDocument(ANdata_serialized)
        A = ANdata.diffiehellman.a
        N = ANdata.diffiehellman.n
        data = ANdata.diffiehellman.data

        mkAB_int = pow(self.publickey(A).y, self.privatekey().x, self.privatekey().p)
        mkAB = number.long_to_bytes(mkAB_int)
        skAB = HMAC.new(mkAB, N, SHA256).digest()

        M_calculated = HMAC.new(skAB, ''.join(P), SHA256).digest()
        if M != M_calculated:
            raise RuntimeError('MAC is invalid')

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