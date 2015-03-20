__author__ = 'shunghsiyu'

class Original:
    def __init__(self):
        print('init')

    def enc(self, data, A, B):
        print('enc')

    def dec(self, payload):
        print('dec')

raise NotImplementedError()