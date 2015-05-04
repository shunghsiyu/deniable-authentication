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
import base64
import pyxb

__author__ = 'shunghsiyu'


class DiffieHellman(Original):
    def __init__(self, identity):
        super(DiffieHellman, self).__init__(identity)
        self._n = 16

    def enc(self, data, A, B):
        # 0) Ensure the encoding of A and B is UTF-8
        A = unicode(A).encode('utf-8')
        B = unicode(B).encode('utf-8')

        # 1) Pick a random value r
        r = Random.get_random_bytes(self._n)
        r_int = number.bytes_to_long(r)

        # 2) Generate master key for B
        # mk_AB = (g^X_B)^X_A
        mkAB_int = pow(self.publickey(B).y, self.privatekey().x, self.privatekey().p)

        # 3) Generate session key k_AB
        ## 3.1) Generate PRF key prf_key
        ## k = (mk_AB)^r
        prf_key_int = pow(mkAB_int, r_int, self.privatekey().p)
        prf_key = number.long_to_bytes(prf_key_int)

        ## 3.2) Calcuate the session key with HMAC with prf_key as key
        k = HMAC.new(prf_key, 0, SHA256).digest()

        # 4) Encrypt A, r, k and data with public key of the receiver
        ## 4.1) Serialize A, r, k and data
        Arkdata_serialized = containerxml.container(a=A, r=r, k=k, data=data).toxml('utf-8')

        ## 4.2) Generate keys for AES and HMAC
        ### 4.2.1) Generate a main key t
        t = Random.get_random_bytes(self._n)

        ### 4.2.2) Derive hmac_key and aes_key from t
        hmac_key = HMAC.new(t, '\x00', SHA256).digest()
        aes_key  = HMAC.new(t, '\x01', SHA256).digest()

        ## 4.3) Encrypt serialized A, r, k and data using AES with aes_key as key
        iv = self._iv()
        aest = AES.new(aes_key, AES.MODE_CTR, counter=self._ctr(iv))
        C = aest.encrypt(Arkdata_serialized)

        ## 4.4) Encrypt main key t using ElGamal with public key of receiver
        nonce = random.randint(1+1, self.privatekey().p-1-1)
        csession_tuple = self.publickey(B).encrypt(t, nonce)
        csession = ''.join(csession_tuple)

        ## 4.5) Calculate the MAC of csession and C
        mac = HMAC.new(hmac_key, ''.join([csession, C]), SHA256).digest()

        c = pyxb.BIND(C, hmac=base64.b64encode(mac), csession=base64.b64encode(csession), iv=iv)
        payload_serialized = payloadxml.payload(c=c).toxml('utf-8')
        return payload_serialized

    def dec(self, payload_serialized):
        # Deserialize payload to obtain C, IV, MAC and ciphertext of main key t (csession)
        payload = payloadxml.CreateFromDocument(payload_serialized)
        C = payload.c.value()
        iv = payload.c.iv
        mac = payload.c.hmac
        csession = payload.c.csession
        split_length = len(csession)/2
        csession_tuple = (csession[:split_length], csession[split_length:])

        # Decrypt csession to obtain t
        t = self.privatekey().decrypt(csession_tuple)

        # Derive the key for HMAC and AES
        hmac_key = HMAC.new(t, '\x00', SHA256).digest()
        aes_key  = HMAC.new(t, '\x01', SHA256).digest()

        # Verify the MAC
        mac_calculated = HMAC.new(hmac_key, ''.join([csession, C]), SHA256).digest()
        if not self.isEqual(mac_calculated, mac):
            raise RuntimeError('HMAC is invalid')

        # Decrypt C to obtain serialized A, r, k and data
        aest = AES.new(aes_key, AES.MODE_CTR, counter=self._ctr(iv))
        Arkdata_serialized = aest.decrypt(C)

        # Deserialize to obtain A, r, k and data
        Arkdata = containerxml.CreateFromDocument(Arkdata_serialized)
        A = Arkdata.a
        r = Arkdata.r
        k = Arkdata.k
        data = Arkdata.data

        # TODO: Anything else to check here?

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