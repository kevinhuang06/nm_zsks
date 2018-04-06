#coding=utf-8

from zsks import NmZsks


class TouDang(NmZsks):

    def __init__(self):
        super(TouDang, self).__init__()
        self.tname = '1ben_bu_toudang_record'

    def insert_into_toudang(self, data):
        self.insert_into_table(data, self.tname)

