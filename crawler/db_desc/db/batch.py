#coding=utf-8

import MySQLdb


class Batch(object):

    def __init__(self):
        self.conn = MySQLdb.connect(host="localhost",user="root",db="zsks", charset='utf8')
        self.conn.ping(True)
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def insert_into_table(self, data, table):
        keys = []
        values = []
        for k in data:
            if data[k] is not None:
                keys.append(k)
                value = data[k].encode('utf-8')
                if value.isdigit():
                    values.append(value)
                else:
                    values.append('\'{0}\''.format(value))
                #print k, data[k].encode('utf-8')
        sql = 'insert ignore into {0} ({1}) VALUES({2})'.format(table, ','.join(keys), ','.join(values))
        print sql
        self.cursor.execute(sql)
        self.conn.commit()

