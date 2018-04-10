#coding=utf-8

import MySQLdb

conf_name = 'test'
from config import app_config

class NmZsks(object):

    def __init__(self):
	self.conn = MySQLdb.connect(
	    host=app_config[conf_name].MYSQL_DATABASE_HOST,
	    user=app_config[conf_name].MYSQL_DATABASE_USER,
	    passwd=app_config[conf_name].MYSQL_DATABASE_PASSWORD,
	    db=app_config[conf_name].MYSQL_DATABASE_DB,
	    charset='utf8'
	)
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
if __name__ == '__main__':
    nm = NmZsks()
