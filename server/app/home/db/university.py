#coding=utf-8

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

from zsks import NmZsks

class University(NmZsks):

    def __init__(self):
        super(University, self).__init__()
        self.tname = 'university'

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

    def batch_id(self, major, batch):
        sql = 'select id from batch where high_school_major = \'{}\' and batch_name=\'{}\''.format(major, batch)
        print sql
        self.cursor.execute(sql)
        self.conn.commit()
        res = self.cursor.fetchone()
        print res[0]
        return res[0]

    def university_can_apply(self, score, batch, high_school_major):
        major_map = {
            'wen_ke': '普通文科',
            'li_ke': '普通理科',
            'yi_ben': '本科一批',
            'er_ben': '本科二批'
        }
        bid = self.batch_id(major_map[high_school_major], major_map[batch])
        i_score = int(score)
        sql = 'select name,min_score_1vs1 from university where min_score_1vs1 > {} and min_score_1vs1 < {}\
         and batch_id={} order by min_score_1vs1 desc'.format(
            i_score-15, i_score+15,bid
        )
        print sql
        self.cursor.execute(sql)
        self.conn.commit()
        res = []
        for name, min_score_1vs1 in self.cursor.fetchall():
            print name, min_score_1vs1
            res.append((name.encode('utf-8'), int(min_score_1vs1)))
        return res


if __name__ == '__main__':
    uni = University()
    uni.university_can_apply(555, 'yi_ben', 'li_ke')