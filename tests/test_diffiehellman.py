#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'shunghsiyu'
import string
import unittest
import os
from deniable.diffiehellman import DiffieHellman
from Crypto import Random
from Crypto.Random import random
from Crypto.PublicKey import ElGamal
from Crypto.PublicKey.ElGamal import ElGamalobj
from deniable.utils import export_elgamal_key


class TestDiffieHellman(unittest.TestCase):

    NUM_BITS = 512

    @classmethod
    def setUpClass(cls):
        cls.A = ''.join(random.choice(string.ascii_letters) for _ in range(12))
        cls.B = ''.join(random.choice(string.ascii_letters) for _ in range(12))
        keyA = ElGamal.generate(cls.NUM_BITS, Random.new().read)
        with open(cls.A, 'w') as f:
            f.write(export_elgamal_key(keyA))
        with open(cls.A+'.pub', 'w') as f:
            f.write(export_elgamal_key(keyA.publickey()))

        x = random.randint(1+1, keyA.p-1-1)
        y = pow(keyA.g, x, keyA.p)
        tup = (keyA.p, keyA.g, y, x)
        keyB = ElGamal.construct(tup)
        with open(cls.B, 'w') as f:
            f.write(export_elgamal_key(keyB))
        with open(cls.B+'.pub', 'w') as f:
            keyB = ElGamal.construct(tup)
            f.write(export_elgamal_key(keyB.publickey()))

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.A)
        os.remove(cls.A+'.pub')
        os.remove(cls.B)
        os.remove(cls.B+'.pub')

    def test_read_private(self):
        private_key = DiffieHellman(self.A).privatekey()
        self.assertIsNotNone(private_key)
        self.assertIsInstance(private_key, ElGamalobj)
        self.assertTrue(private_key.has_private())

    def test_read_public(self):
        public_key = DiffieHellman(self.A).publickey(self.B)
        self.assertIsNotNone(public_key)
        self.assertIsInstance(public_key, ElGamalobj)

    def test_pg(self):
        private_keyA = DiffieHellman(self.A).privatekey()
        public_keyB = DiffieHellman(self.A).publickey(self.B)
        self.assertEqual(private_keyA.p, public_keyB.p)
        self.assertEqual(private_keyA.g, public_keyB.g)

    def test_enc_toself(self):
        data = '123'
        cipher_text = DiffieHellman(self.A).enc(data, self.A)
        self.assertIsNotNone(cipher_text)

    def test_dec_fromself(self):
        data = u'this is a unicode string with chinese for testing the code\n這是中文'.encode('utf-8')
        cipher_text = DiffieHellman(self.A).enc(data, self.A)
        plain_text = DiffieHellman(self.A).dec(cipher_text)
        self.assertIsNotNone(plain_text)
        self.assertEqual(data, plain_text)

    def test_dec_from_b(self):
        data = u'this is a unicode string with chinese for testing the code\n這是中文'.encode('utf-8')
        cipher_text = DiffieHellman(self.B).enc(data, self.A)
        plain_text = DiffieHellman(self.A).dec(cipher_text)
        self.assertIsNotNone(plain_text)
        self.assertEqual(data, plain_text)

    def test_enc_toself_b64(self):
        data = '123'
        cipher_text = DiffieHellman(self.A).enc(data, self.A)
        self.assertIsNotNone(cipher_text)

    def test_dec_fromself_b64(self):
        data = u'this is a unicode string with chinese for testing the code\n這是中文'.encode('utf-8')
        cipher_text_b64 = DiffieHellman(self.A).enc_base64(data, self.A)
        plain_text = DiffieHellman(self.A).dec_base64(cipher_text_b64)
        self.assertIsNotNone(plain_text)
        self.assertEqual(data, plain_text)


if __name__ == '__main__':
    unittest.main()

