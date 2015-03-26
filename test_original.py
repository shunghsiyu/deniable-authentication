import unittest
import random
import string
import os
from original import Original
from Crypto.PublicKey import RSA
from Crypto.PublicKey.RSA import _RSAobj

__author__ = 'shunghsiyu'


class TestOriginal(unittest.TestCase):

    NUM_BITS = 2048

    def setUp(self):
        self.A = ''.join(random.choice(string.ascii_letters) for _ in range(12))
        self.B = ''.join(random.choice(string.ascii_letters) for _ in range(12))
        rsaA = RSA.generate(self.NUM_BITS)
        with open(self.A, 'w') as f:
            f.write(rsaA.exportKey('PEM'))
        with open(self.A+'.pub', 'w') as f:
            f.write(rsaA.publickey().exportKey('PEM'))
        with open(self.B+'.pub', 'w') as f:
            rsaB = RSA.generate(self.NUM_BITS).publickey()
            f.write(rsaB.exportKey('PEM'))
        self.object = Original(self.A)

    def tearDown(self):
        os.remove(self.A)
        os.remove(self.A+'.pub')
        os.remove(self.B+'.pub')

    def test_enc(self):
        self.fail('Not implemented')

    def test_dec(self):
        self.fail('Not implemented')

    def test_publickey(self):
        public_key = self.object.publickey(self.B)
        self.assertIsNotNone(public_key, 'Must be able to find public key')
        self.assertIsInstance(public_key, _RSAobj)

    def test_privatekey(self):
        private_key = self.object.privatekey()
        self.assertIsNotNone(private_key, 'Must have a private key')
        self.assertIsInstance(private_key, _RSAobj)
        self.assertTrue(private_key.has_private())

if __name__ == '__main__':
    unittest.main()