#!/usr/bin/python
# -*- coding: utf-8 -*-
from Crypto import Random
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Cipher.PKCS1_OAEP import PKCS1OAEP_Cipher
from Crypto.Hash import HMAC, SHA256
from Crypto.PublicKey import RSA
from Crypto.PublicKey.RSA import _RSAobj
from Crypto.Signature import PKCS1_PSS
from Crypto.Signature.PKCS1_PSS import PSS_SigScheme
from Crypto.Util import Counter
from gen import payloadxml, containerxml
import base64
import pyxb

__author__ = 'shunghsiyu'

class Original(object):
    def __init__(self, identity):
        self._identity = identity
        self._n = 16
        self._iv = 1L

    def _ctr(self, iv=None):
        if iv is None:
            iv = self._iv
        return Counter.new(128, initial_value=iv)

    def enc(self, data, A, B):
        # 1) Pick a random session key
        ## krand <- {0, 1}^n
        k = Random.get_random_bytes(self._n)

        # 2) Encrypt data
        ## D <- e[data]krand
        aesk = AES.new(k, AES.MODE_CTR, counter=self._ctr())
        D = aesk.encrypt(data)

        # 3) Calculate message authentication code of the ciphertext
        ## M = MAC(krand, D)
        hmac = HMAC.new(k, D, SHA256)
        M = hmac.digest()

        # 4.1) Serialize A, B and krand
        ABk_serialized = containerxml.container(pyxb.BIND(a=A, b=B, k=k)).toxml('utf-8')

        # 4.2) Sign the serialization of a container with A, B and krand
        ## S <- signA(A, B, krand)
        priA = self.privatekey()
        signer = PKCS1_PSS.new(priA)
        hashABk = SHA256.new(ABk_serialized)
        S = signer.sign(hashABk)

        # 5.1) Serialize A, B, krand and S
        ABkS_serialized = containerxml.container(pyxb.BIND(a=A, b=B, k=k, s=S)).toxml('utf-8')

        # 5.2) Generate an AES session key t
        t = Random.get_random_bytes(self._n)
        aest = AES.new(t, AES.MODE_CTR, counter=self._ctr())

        # 5.3) Encrypt A, B, krand and S using AES with session key t
        ## H <- e[A, B, krand, S]kt
        H = aest.encrypt(ABkS_serialized)

        # 5.4) Encrypt session key t with public key of receiver
        ## cs <- E{kt}pubB
        pubB = self.publickey(B)
        rsa = PKCS1_OAEP.new(pubB, SHA256)
        cs = rsa.encrypt(t)

        # 6) Serialize H (with cs), D and M
        ## payload = H||D||M
        h = pyxb.BIND(H, csession=base64.b64encode(cs), iv=self._iv)
        payload_serialized = payloadxml.payload(pyxb.BIND(h=h, d=D, m=M)).toxml('utf-8')
        return payload_serialized

    def dec(self, payload_serialized):
        payload = payloadxml.CreateFromDocument(payload_serialized)
        assert isinstance(payload, payloadxml.CTD_ANON)

        priB = self.privatekey()
        assert isinstance(priB, _RSAobj)
        rsa = PKCS1_OAEP.new(priB, SHA256)
        assert isinstance(rsa, PKCS1OAEP_Cipher)
        H = payload.original.h.value()
        t = rsa.decrypt(payload.original.h.csession)
        aest = AES.new(t, AES.MODE_CTR, counter=self._ctr(payload.original.h.iv))
        ABkS_serialized = aest.decrypt(H)
        ABkS = containerxml.CreateFromDocument(ABkS_serialized)
        assert isinstance(ABkS, containerxml.CTD_ANON)

        k = ABkS.original.k
        A = ABkS.original.a
        B = ABkS.original.b
        S = ABkS.original.s
        if not self._checkABk(A, B, k, S):
            raise RuntimeError('Signature and data does not match')

        D = payload.original.d
        M = payload.original.m
        if not self._checkDM(k, D, M):
            raise RuntimeError('MAC and the message does not match')

        aesk = AES.new(k, AES.MODE_CTR, counter=self._ctr())
        data = aesk.decrypt(D)
        return data

    def _checkABk(self, A, B, k, S):
        passed = True
        if B != self._identity:
            passed = False

        # TODO: check if the program is willing to receive stuff from A

        pubA = self.publickey(A)
        assert isinstance(pubA, _RSAobj)
        verifier = PKCS1_PSS.new(pubA)
        assert isinstance(verifier, PSS_SigScheme)

        ABk_serialized = containerxml.container(pyxb.BIND(a=A, b=B, k=k)).toxml('utf-8')
        hashABk = SHA256.new(ABk_serialized)
        if not verifier.verify(hashABk, S):
            passed = False
        return passed

    def _checkDM(self, k, D, M):
        passed = True

        hmac = HMAC.new(k, D, SHA256)
        if M != hmac.digest():
            passed = False

        return passed

    def publickey(self, target):
        with open(target+'.pub', 'r') as f:
            publickey = RSA.importKey(f.read())
        return publickey

    def privatekey(self):
        with open(self._identity, 'r') as f:
            privatekey = RSA.importKey(f.read())
        return privatekey
