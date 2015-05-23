#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
from Crypto import Random
from Crypto.Random import random
from Crypto.PublicKey import ElGamal
from deniable.strong import Strong
from deniable.utils import export_elgamal_key
import argparse
__author__ = 'shunghsiyu'


def gen(args):
    name = unicode(raw_input("Please enter your preferred username: "))
    with open('identity', 'w') as f:
        f.write(name.encode('utf-8'))
    if args.key_size:
        el_gamal = ElGamal.generate(args.key_size, Random.new().read)
    elif args.parameter_from:
        parameters = [int(value) for value in args.parameter_from.read().splitlines()]
        assert len(parameters) >= 2
        p = parameters[0]
        g = parameters[1]
        x = random.randint(1+1, p-1-1)
        y = pow(g, x, p)
        el_gamal = ElGamal.construct((p, g, y, x))
    else:
        raise RuntimeError

    with open(name, 'w') as f:
        f.write(export_elgamal_key(el_gamal))
    with open(name+'.pub', 'w') as f:
        f.write(export_elgamal_key(el_gamal.publickey()))


def enc(args):
    name = args.identity.read().decode('utf-8')
    args.identity.close()
    cipher_text = Strong(name).enc(args.input.read(), args.recipient)
    args.input.close()
    args.output.write(cipher_text)
    args.output.close()


def dec(args):
    name = args.identity.read().decode('utf-8')
    args.identity.close()
    plain_text = Strong(name).dec(args.input.read())
    args.input.close()
    args.output.write(plain_text)
    args.output.close()


parser = argparse.ArgumentParser()
subparser = parser.add_subparsers()

parser_gen = subparser.add_parser('gen')
group = parser_gen.add_mutually_exclusive_group(required=True)
group.add_argument('key_size', type=int, nargs='?')
group.add_argument('-p', '--parameter_from', type=argparse.FileType('r'), nargs='?')
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