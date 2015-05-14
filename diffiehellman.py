#!/usr/bin/python
# -*- coding: utf-8 -*-
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Hash import HMAC, SHA256
from Crypto.PublicKey import ElGamal
from Crypto.Util import number
from Crypto.Random import random
from original import Original
import base64
import cPickle as pickle

__author__ = 'shunghsiyu'


class DiffieHellman(Original):
    def __init__(self, identity):
        super(DiffieHellman, self).__init__(identity)
        self._n = 16

    def enc(self, data, A, B):
        return self._enc(data, A, B)

    def enc_base64(self, data, A, B):
        return base64.b64encode(self._enc(data, A, B))

    def _enc(self, data, A, B):
        # 0) Ensure the encoding of A and B is UTF-8
        A = unicode(A).encode('utf-8')
        B = unicode(B).encode('utf-8')

        # 1) Pick a random value r
        r = Random.get_random_bytes(self._n)
        r_int = number.bytes_to_long(r)

        # 2) Generate session key k_AB
        ## 2.1) Generate PRF key prf_key
        # mk_AB = (g^X_B)^X_A
        mkAB_int = pow(self.publickey(B).y, self.privatekey().x, self.privatekey().p)
        mkAB = number.long_to_bytes(mkAB_int)

        ## 2.2) Calcuate the session key with HMAC with prf_key as key
        k = HMAC.new(mkAB, ''.join([r, B]), SHA256).digest()

        # 3) Encrypt A, r, k and data with public key of the receiver
        ## 3.1) Serialize A, r, k and data
        Arkdata_serialized = pickle.dumps(dict(a=A, r=r, k=k, data=data), pickle.HIGHEST_PROTOCOL)

        ## 3.2) Generate keys for AES and HMAC
        ### 3.2.1) Generate a main key t
        t = Random.get_random_bytes(self._n)

        ### 3.2.2) Derive hmac_key and aes_key from t
        hmac_key = HMAC.new(t, '\x00', SHA256).digest()
        aes_key  = HMAC.new(t, '\x01', SHA256).digest()

        ## 3.3) Encrypt serialized A, r, k and data using AES with aes_key as key
        iv = self._iv()
        aest = AES.new(aes_key, AES.MODE_CTR, counter=self._ctr(iv))
        C = aest.encrypt(Arkdata_serialized)

        ## 3.4) Encrypt main key t using ElGamal with public key of receiver
        nonce = random.randint(1+1, self.privatekey().p-1-1)
        csession_tuple = self.publickey(B).encrypt(t, nonce)
        csession = ''.join(csession_tuple)

        ## 3.5) Calculate the MAC of csession and C
        mac = HMAC.new(hmac_key, ''.join([csession, C]), SHA256).digest()

        payload_serialized = pickle.dumps(dict(c=C, hmac=mac, csession=csession, iv=iv), pickle.HIGHEST_PROTOCOL)
        return payload_serialized

    def dec(self, payload_serialized):
        return self._dec(payload_serialized)

    def dec_base64(self, payload_serialized):
        return self._dec(base64.b64decode(payload_serialized))

    def _dec(self, payload_serialized):
        # Deserialize payload to obtain C, IV, MAC and ciphertext of main key t (csession)
        payload = pickle.loads(payload_serialized)
        C = payload['c']
        iv = payload['iv']
        mac = payload['hmac']
        csession = payload['csession']
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
        Arkdata = pickle.loads(Arkdata_serialized)
        A = Arkdata['a']
        r = Arkdata['r']
        k = Arkdata['k']
        data = Arkdata['data']

        # Generate PRF key prf_key
        mkAB_int = pow(self.publickey(A).y, self.privatekey().x, self.privatekey().p)
        mkAB = number.long_to_bytes(mkAB_int)

        # Calcuate the session key with HMAC with prf_key as key
        k_calculated = HMAC.new(mkAB, ''.join([r, self._identity]), SHA256).digest()

        # Verify the session key
        if not self.isEqual(k, k_calculated):
            raise RuntimeError('Session key is invalid')

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