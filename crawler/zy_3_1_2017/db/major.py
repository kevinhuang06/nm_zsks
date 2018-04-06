#coding=utf-8

from zsks import NmZsks


class Major(NmZsks):

    def __init__(self):
        super(Major, self).__init__()
        self.tname = '1ben_major'

    def insert_into_major(self, data):

        self.insert_into_table(data, self.tname)