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
        # Deserialize payload
        payload = payloadxml.CreateFromDocument(payload_serialized)

        # Decrypt AES session key t with the receiver's private key
        priB = self.privatekey()
        rsa = PKCS1_OAEP.new(priB, SHA256)
        t = rsa.decrypt(payload.h.csession)

        # Decrypt cipher-text H with AES session key t to obtain
        # the serialized container with A, B, krand and S
        H = payload.h.value()
        aest = AES.new(t, AES.MODE_CTR, counter=self._ctr(payload.h.iv))
        ABkS_serialized = aest.decrypt(H)

        # Deserialize the container with A, B, krand and S
        # and retrieve values of A, B, krand and S
        ABkS = containerxml.CreateFromDocument(ABkS_serialized)
        k = ABkS.k
        A = ABkS.a
        B = ABkS.b
        S = ABkS.s

        # Checks A, B, krand against signature S
        if not self._checkABk(A, B, k, S):
            raise RuntimeError('Signature and data does not match')

        # Retrieve values of D and M
        D = payload.d
        M = payload.m

        # Checks HMAC of D with key krand against M
        if not self._checkDM(k, D, M):
            raise RuntimeError('MAC and the message does not match')

        # Decrypt cipher-text D to retrieve data
        aesk = AES.new(k, AES.MODE_CTR, counter=self._ctr())
        data = aesk.decrypt(D)
        return data

    def _checkABk(self, A, B, k, S):
        passed = True

        # Abort if this program is not the targeted receiver
        if B != self._identity:
            passed = False
            return passed

        # TODO: check if the program is willing to receive stuff from A

        # Serialize A, B and krand the same way enc() serialize it
        # and calculate its hash value
        ABk_serialized = containerxml.container(pyxb.BIND(a=A, b=B, k=k)).toxml('utf-8')
        hashABk = SHA256.new(ABk_serialized)

        # Obtain the public key of the sender to verify that the hash value
        # matches the signature
        pubA = self.publickey(A)
        verifier = PKCS1_PSS.new(pubA)

        # Return true if the signature matches the hash value
        # and false if otherwise
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
