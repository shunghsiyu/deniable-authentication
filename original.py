#!/usr/bin/python
# -*- coding: utf-8 -*-
from Crypto import Random
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Hash import HMAC, SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_PSS
from Crypto.Util import Counter
from gen import original_payloadxml as payloadxml, original_containerxml as containerxml
import base64
import pyxb

__author__ = 'shunghsiyu'

class Original(object):
    def __init__(self, identity):
        self._identity = identity
        self._n = 16

    def _iv(self):
        return 1L

    def _ctr(self, iv=None):
        if iv is None:
            iv = self._iv
        return Counter.new(128, initial_value=iv)

    def enc(self, data, A, B):
        # 0) Ensure the encoding of A and B is UTF-8
        A = unicode(A).encode('utf-8')
        B = unicode(B).encode('utf-8')

        # 1) Pick a random nonce
        # N_A <- {0, 1}^n
        N = Random.get_random_bytes(self._n)

        # 2) Sign to value of B concatenated with N_A
        # S <- sign_A(B, N_A)
        priA = self.privatekey()
        signer = PKCS1_PSS.new(priA)
        hashBN = SHA256.new(''.join([B, N]))
        S = signer.sign(hashBN)

        # 3) CCA-Secure encryption of A, N, S and data
        # C <- E_pub_B(A, N_A, S, data)
        ## 3.1) Serialize A, N, S and data
        ANSdata_serialized = containerxml.container(a=A, n=N, s=S, data=data).toxml('utf-8')

        ## 3.2) Encrypt serialized data
        ### 3.2.1) Generate an AES session key t
        t = Random.get_random_bytes(self._n)

        ### 3.2.2) Generate a random IV
        iv = self._iv()
        aest = AES.new(t, AES.MODE_CTR, counter=self._ctr(iv))

        ### 3.2.3) Encrypt data to obtain ciphertext of serialization
        C = aest.encrypt(ANSdata_serialized)

        ### 3.2.4) Calculate HMAC of cdata with secret key t (same as AES session key)
        hmac = HMAC.new(t, C, SHA256).digest()

        ### 3.2.5) Encrypt session key t with RSA-OAEP
        pubB = self.publickey(B)
        rsa = PKCS1_OAEP.new(pubB, SHA256)
        csession = rsa.encrypt(t)

        # 4) Prepare the payload
        c = pyxb.BIND(C, hmac=base64.b64encode(hmac), csession=base64.b64encode(csession), iv=iv)
        payload_serialized = payloadxml.payload(c=c).toxml('utf-8')

        return payload_serialized

    def dec(self, payload_serialized):
        # Deserialize payload and obtain C, csession, hmac and iv
        payload = payloadxml.CreateFromDocument(payload_serialized)
        C = payload.c.value()
        csession = payload.c.csession
        hmac = payload.c.hmac
        iv = payload.c.iv

        # Decrypt AES session key t with the receiver's private key
        priB = self.privatekey()
        rsa = PKCS1_OAEP.new(priB, SHA256)
        t = rsa.decrypt(csession)

        # Check C against its HMAC
        hmac_calculated = HMAC.new(t, C, SHA256).digest()
        if not self.isEqual(hmac_calculated, hmac):
            raise RuntimeError('HMAC does not match C')

        # Decrypt cipher-text C with AES session key t to obtain
        # the serialized container with A, N, S and data
        aest = AES.new(t, AES.MODE_CTR, counter=self._ctr(iv))
        ANSdata_serialized = aest.decrypt(C)

        # Deserialize the container with A, N, S and data
        # and retrieve values of A, N, S and data
        ANSdata = containerxml.CreateFromDocument(ANSdata_serialized)
        A = ANSdata.a
        N = ANSdata.n
        S = ANSdata.s
        data = ANSdata.data

        # Verify the signature S against B and N
        pubA = self.publickey(A)
        verifier = PKCS1_PSS.new(pubA)
        hashBN = SHA256.new(''.join([self._identity, N]))
        if not verifier.verify(hashBN, S):
            raise RuntimeError('S does not match B and N')

        return data

    def publickey(self, target):
        with open(target+'.pub', 'r') as f:
            publickey = RSA.importKey(f.read())
        return publickey

    def privatekey(self):
        with open(self._identity, 'r') as f:
            privatekey = RSA.importKey(f.read())
        return privatekey

    def isEqual(self, a, b):
        # Mitigate timing attack
        # from: http://codahale.com/a-lesson-in-timing-attacks/

        if len(a) != len(b):
            return False

        result = 0
        for x, y in zip(a, b):
            result |= ord(x) ^ ord(y)

        return result == 0