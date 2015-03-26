from Crypto import Random
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Cipher.PKCS1_OAEP import PKCS1OAEP_Cipher
from Crypto.Hash import HMAC, SHA256
from Crypto.PublicKey import RSA
from Crypto.PublicKey.RSA import _RSAobj
from Crypto.Signature import PKCS1_PSS
from Crypto.Signature.PKCS1_PSS import PSS_SigScheme
from Crypto.Util import Counter
from payload import Payload, Container
import pickle

__author__ = 'shunghsiyu'

class Original:
    def __init__(self, identity):
        self._identity = identity
        self._n = 32
        self._iv = 1L

    def _ctr(self):
        return Counter.new(128, initial_value=self._iv)

    def enc(self, data, A, B):
        priA = self.privatekey()
        assert isinstance(priA, _RSAobj)
        pubB = self.publickey(B)
        assert isinstance(pubB, _RSAobj)
        signer = PKCS1_PSS.new(priA)
        assert isinstance(signer, PSS_SigScheme)
        rsa = PKCS1_OAEP.new(pubB, SHA256)
        assert isinstance(rsa, PKCS1OAEP_Cipher)

        k = Random.get_random_bytes(self._n)

        aesk = AES.new(k, AES.MODE_CTR, counter=self._ctr())
        D = aesk.encrypt(data)

        hmac = HMAC.new(k, D, SHA256)
        M = hmac.digest()

        ABk_serialized = Container(A, B, k).serialize()
        hashABk = SHA256.new(ABk_serialized)
        S = signer.sign(hashABk)

        t = k
        aest = AES.new(t, AES.MODE_CTR, counter=self._ctr())
        ABkS_serialized = Container(A, B, k, S).serialize()
        H = aest.encrypt(ABkS_serialized)
        payload = Payload(H, D, M, ct=rsa.encrypt(t))
        return payload.serialize()

    def dec(self, payload_serialized):
        payload = pickle.loads(payload_serialized)
        assert isinstance(payload, Payload)

        priB = self.privatekey()
        assert isinstance(priB, _RSAobj)
        rsa = PKCS1_OAEP.new(priB, SHA256)
        assert isinstance(rsa, PKCS1OAEP_Cipher)
        H = payload.H()
        t = rsa.decrypt(payload.ct())
        aest = AES.new(t, AES.MODE_CTR, counter=self._ctr())
        ABkS_serialized = aest.decrypt(H)
        ABkS = pickle.loads(ABkS_serialized)
        assert isinstance(ABkS, Container)

        k = ABkS.k()
        A = ABkS.A()
        B = ABkS.B()
        S = ABkS.S()
        if not self._checkABk(A, B, k, S):
            raise RuntimeError('Signature and data does not match')

        D = payload.D()
        M = payload.M()
        if not self._checkDM(k, D, M):
            raise RuntimeError('MAC and the message does not match')

        aesk = AES.new(k, AES.MODE_CTR, counter=self._ctr())
        data = aesk.decrypt(D)
        return data

    def _checkABk(self, A, B, k, S):
        passed = True
        if B != self._identity:
            passed = False

        # TODO: check if the program is willing to receive stuff from A

        pubA = self.publickey(A)
        assert isinstance(pubA, _RSAobj)
        verifier = PKCS1_PSS.new(pubA)
        assert isinstance(verifier, PSS_SigScheme)

        ABk_serialized = Container(A, B, k).serialize()
        hashABk = SHA256.new(ABk_serialized)
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
