#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest
import random
import string
import os
import pyxb
from gen import containerxml
from original import Original
from Crypto.PublicKey import RSA
from Crypto.PublicKey.RSA import _RSAobj

__author__ = 'shunghsiyu'


class TestOriginal(unittest.TestCase):

    NUM_BITS = 2048

    @classmethod
    def setUpClass(cls):
        cls.A = ''.join(random.choice(string.ascii_letters) for _ in range(12))
        cls.B = ''.join(random.choice(string.ascii_letters) for _ in range(12))
        rsaA = RSA.generate(cls.NUM_BITS)
        with open(cls.A, 'w') as f:
            f.write(rsaA.exportKey('PEM'))
        with open(cls.A+'.pub', 'w') as f:
            f.write(rsaA.publickey().exportKey('PEM'))
        with open(cls.B+'.pub', 'w') as f:
            rsaB = RSA.generate(cls.NUM_BITS).publickey()
            f.write(rsaB.exportKey('PEM'))

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.A)
        os.remove(cls.A+'.pub')
        os.remove(cls.B+'.pub')

    def test_serialize_container(self):
        n_bits = 256
        A = 'A'
        B = 'B'
        k = bin(random.getrandbits(n_bits))
        S = bin(random.getrandbits(n_bits))
        serialized = containerxml.container(pyxb.BIND(a=A,b=B, k=k, s=S)).toxml('utf-8')
        unserialized = containerxml.CreateFromDocument(serialized)
        self.assertIsInstance(unserialized, containerxml.CTD_ANON)
        self.assertEqual(unserialized.original.a, A)
        self.assertEqual(unserialized.original.b, B)
        self.assertEqual(unserialized.original.k, k)
        self.assertEqual(unserialized.original.s, S)

    def test_enc_toself(self):
        data = '123'
        cipher_text = Original(self.A).enc(data, self.A, self.A)
        self.assertIsNotNone(cipher_text)

    def test_dec_fromself(self):
        data = u'this is a unicode string with chinese for testing the code\n這是中文'.encode('utf-8')
        cipher_text = Original(self.A).enc(data, self.A, self.A)
        plain_text = Original(self.A).dec(cipher_text)
        self.assertIsNotNone(plain_text)
        self.assertEqual(data, plain_text)

    def test_publickey(self):
        public_key = Original(self.A).publickey(self.B)
        self.assertIsNotNone(public_key, 'Must be able to find public key')
        self.assertIsInstance(public_key, _RSAobj)

    def test_privatekey(self):
        private_key = Original(self.A).privatekey()
        self.assertIsNotNone(private_key, 'Must have a private key')
        self.assertIsInstance(private_key, _RSAobj)
        self.assertTrue(private_key.has_private())

if __name__ == '__main__':
    unittest.main()