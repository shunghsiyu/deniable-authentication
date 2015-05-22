#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
from Crypto.PublicKey import RSA
from deniable.original import Original
import argparse
__author__ = 'shunghsiyu'

def gen(args):
    name = unicode(raw_input("Please enter your preferred username: "))
    with open('identity', 'w') as f:
        f.write(name.encode('utf-8'))
    rsaA = RSA.generate(args.key_size)
    with open(name, 'w') as f:
        f.write(rsaA.exportKey('PEM'))
    with open(name+'.pub', 'w') as f:
        f.write(rsaA.publickey().exportKey('PEM'))


def enc(args):
    name = args.identity.read().decode('utf-8')
    args.identity.close()
    cipher_text = Original(name).enc(args.input.read(), args.recipient)
    args.input.close()
    args.output.write(cipher_text)
    args.output.close()


def dec(args):
    name = args.identity.read().decode('utf-8')
    args.identity.close()
    plain_text = Original(name).dec(args.input.read())
    args.input.close()
    args.output.write(plain_text)
    args.output.close()


parser = argparse.ArgumentParser()
subparser = parser.add_subparsers()

parser_gen = subparser.add_parser('gen')
parser_gen.add_argument('key_size', type=int)
parser_gen.set_defaults(func=gen)

parser_enc = subparser.add_parser('enc')
parser_enc.add_argument('--identity', type=argparse.FileType('r'), default='identity')
parser_enc.add_argument('recipient', type=str)
parser_enc.add_argument('input', type=argparse.FileType('rb'))
parser_enc.add_argument('output', type=argparse.FileType('wb'), default='-', nargs='?')
parser_enc.set_defaults(func=enc)

parser_dec = subparser.add_parser('dec')
parser_dec.add_argument('--identity', type=argparse.FileType('r'), default='identity')
parser_dec.add_argument('input', type=argparse.FileType('rb'))
parser_dec.add_argument('output', type=argparse.FileType('wb'), default='-', nargs='?')
parser_dec.set_defaults(func=dec)

args = parser.parse_args()
args.func(args)