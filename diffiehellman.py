#!/usr/bin/python
# -*- coding: utf-8 -*-
from gen import diffiehellman_containerxml as containerxml, diffiehellman_payloadxml as payloadxml
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
        mkAB_int = pow(self.publickey(B).y, self.privatekey().x, self.privatekey().p)
        mkAB = number.long_to_bytes(mkAB_int)
        N = Random.get_random_bytes(len(mkAB))
        skAB = number.long_to_bytes(number.bytes_to_long(mkAB) ^ number.bytes_to_long(N))

        K = random.randint(1+1, self.privatekey().p-1-1)
        ANdata_serialized = containerxml.container(a=A, n=N, data=data).toxml('utf-8')
        t = Random.get_random_bytes(self._n)
        iv = self._iv()
        aest = AES.new(t, AES.MODE_CTR, counter=self._ctr(iv))
        C = aest.encrypt(ANdata_serialized)

        P = self.publickey(B).encrypt(t, K)
        assert len(P) == 2
        M = HMAC.new(skAB, ''.join(P), SHA256).digest()

        payload_serialized = payloadxml.payload(p1=P[0], p2=P[1], c=C, m=M).toxml('utf-8')
        return payload_serialized

    def dec(self, payload_serialized):
        payload = payloadxml.CreateFromDocument(payload_serialized)
        P1 = str(payload.p1)
        P2 = str(payload.p2)
        P = (P1, P2)
        C = payload.c
        M = payload.m

        t = self.privatekey().decrypt(P)
        iv = self._iv()
        aest = AES.new(t, AES.MODE_CTR, counter=self._ctr(iv))
        ANdata_serialized = aest.decrypt(C)
        print(ANdata_serialized)
        # TODO: Mitigate timing-attack
        ANdata = containerxml.CreateFromDocument(ANdata_serialized)
        A = ANdata.a
        N = ANdata.n
        data = ANdata.data

        mkAB_int = pow(self.publickey(A).y, self.privatekey().x, self.privatekey().p)
        mkAB = number.long_to_bytes(mkAB_int)
        skAB = number.long_to_bytes(number.bytes_to_long(mkAB) ^ number.bytes_to_long(N))

        M_calculated = HMAC.new(skAB, ''.join(P), SHA256).digest()
        if M != M_calculated:
            raise RuntimeError('MAC is invalid')

        return data

    def publickey(self, target):
        # TODO: Work on both certificate and name
        with open(target+'.pub', 'r') as f:
            publickey = ElGamal.construct(tuple(int(value) for value in f.read().splitlines()))
        return publickey

    def privatekey(self):
        with open(self._identity, 'r') as f:
            privatekey = ElGamal.construct(tuple(int(value) for value in f.read().splitlines()))
        assert privatekey.has_private()
        return privatekey