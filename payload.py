import pickle

__author__ = 'shunghsiyu'

class Payload(object):
    def __init__(self, H, D, M):
        _H = H
        _D = D
        _M = M

    def D(self):
        return _D


    def H(self):
        return _H

    def M(self):
        return _M

    def serialize(self):
        return pickle.dump(self)

class Container(object):
    def __init__(self, A, B, k, S = None):
        _A = A
        _B = B
        _k = k
        _S = S

    def A(self):
        return _A

    def B(self):
        return _B

    def k(self):
        return _k

    def S(self):
        return _S

    def serialize(self):
        return pickle.dump(self)
