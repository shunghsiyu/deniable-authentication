import unittest
import random
import string
import os
import pickle
from original import Original
from payload import Container
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

    def test_pickle_Container(self):
        A = 'A'
        B = 'B'
        k = random.getrandbits(256)
        S = 'S'
        serialized = pickle.dumps(Container(A, B, k, S))
        unserialized = pickle.loads(serialized)
        self.assertIsInstance(unserialized, Container)
        self.assertEqual(unserialized.A(), A)
        self.assertEqual(unserialized.B(), B)
        self.assertEqual(unserialized.k(), k)
        self.assertEqual(unserialized.S(), S)

    def test_enc_toself(self):
        data = '123'
        cipher_text = self.object.enc(data, self.A, self.A)
        self.assertIsNotNone(cipher_text)

    def test_dec_fromself(self):
        data = '123'
        cipher_text = self.object.enc(data, self.A, self.A)
        plain_text = self.object.dec(cipher_text)
        self.assertIsNotNone(plain_text)
        self.assertEqual(data, plain_text)

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