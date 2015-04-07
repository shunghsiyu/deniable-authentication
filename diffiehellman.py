#!/usr/bin/python
# -*- coding: utf-8 -*-
from original import Original

__author__ = 'shunghsiyu'


class DiffieHellman(Original):
    def __init__(self, identity):
        super(DiffieHellman, self).__init__(identity)

    def enc(self, data, A, B):
        raise NotImplementedError()

    def dec(self, payload_serialized):
        raise NotImplementedError()
