import pickle

__author__ = 'shunghsiyu'

class Payload(object):
    def __init__(self, H, D, M):
        self._H = H
        self._D = D
        self._M = M

    def D(self):
        return self._D


    def H(self):
        return self._H

    def M(self):
        return self._M

    def serialize(self):
        return pickle.dumps(self)

class Container(object):
    def __init__(self, A, B, k, S = None):
       self._A = A
       self._B = B
       self._k = k
       self._S = S

    def A(self):
        return self._A

    def B(self):
        return self._B

    def k(self):
        return self._k

    def S(self):
        return self._S

    def serialize(self):
        return pickle.dumps(self)
