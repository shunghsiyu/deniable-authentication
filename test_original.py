import unittest
import random
import string
import os
from original import Original
from Crypto.PublicKey import RSA

__author__ = 'shunghsiyu'


class TestOriginal(unittest.TestCase):

    NUM_BITS = 2048

    def setUp(self):
        self.A = ''.join(random.choice(string.ascii_letters) for _ in range(12))
        self.B = ''.join(random.choice(string.ascii_letters) for _ in range(12))
        with open(self.A, 'w') as f:
            rsa = RSA.generate(self.NUM_BITS)
            f.write(rsa.exportKey('PEM'))
        with open(self.B+'.pub', 'w') as f:
            rsa = RSA.generate(self.NUM_BITS).publickey()
            f.write(rsa.exportKey('PEM'))

    def tearDown(self):
        os.remove(self.A)
        os.remove(self.B+'.pub')

    def test_enc(self):
        self.fail('Not implemented')

    def test_dec(self):
        self.fail('Not implemented')

    def test_publickey(self):
        self.fail('Not implemented')

    def test_privatekey(self):
        self.fail('Not implemented')

if __name__ == '__main__':
    unittest.main()