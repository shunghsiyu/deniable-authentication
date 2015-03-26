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
        cipher_text = Original(self.A).enc(data, self.A, self.A)
        self.assertIsNotNone(cipher_text)

    def test_dec_fromself(self):
        data = '123'
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