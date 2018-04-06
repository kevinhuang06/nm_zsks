#coding=utf-8

from zsks import NmZsks

class University(NmZsks):

    def __init__(self):
        super(University, self).__init__()
        self.tname = '1ben_bu_university'

    def insert_into_university(self, data):

        self.insert_into_table(data, self.tname)

    def get_major_details(self):
        sql = 'select id,name,major_detail_url from {}'.format(self.tname)
        self.cursor.execute(sql)
        self.conn.commit()
        for s in self.cursor.fetchall():
            yield s

    def get_toudang_details(self):
        sql = 'select id, name, toudang_detail_url from {}'.format(self.tname)
        self.cursor.execute(sql)
        self.conn.commit()
        for s in self.cursor.fetchall():
            yield s