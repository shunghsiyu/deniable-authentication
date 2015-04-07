#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'shunghsiyu'

import os
import random
import string
import unittest
from diffiehellman import DiffieHellman
from Crypto import Random
from Crypto.PublicKey import ElGamal
from Crypto.PublicKey.ElGamal import ElGamalobj


def export_key(key):
    assert isinstance(key, ElGamalobj)
    if hasattr(key, 'x'):
        key_info = (key.p, key.g, key.y, key.x)
    else:
        key_info = (key.p, key.g, key.y)
    return '\n'.join(str(n) for n in key_info)


class TestDiffieHellman(unittest.TestCase):

    NUM_BITS = 512

    @classmethod
    def setUpClass(cls):
        cls.A = ''.join(random.choice(string.ascii_letters) for _ in range(12))
        cls.B = ''.join(random.choice(string.ascii_letters) for _ in range(12))
        keyA = ElGamal.generate(cls.NUM_BITS, Random.new().read)
        with open(cls.A, 'w') as f:
            f.write(export_key(keyA))
        with open(cls.A+'.pub', 'w') as f:
            f.write(export_key(keyA.publickey()))
        with open(cls.B+'.pub', 'w') as f:
            keyB = ElGamal.generate(cls.NUM_BITS, Random.new().read)
            f.write(export_key(keyB.publickey()))

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.A)
        os.remove(cls.A+'.pub')
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


if __name__ == '__main__':
    unittest.main()

