#coding=utf-8


from db.batch import Batch




filed = ['major_code','batch_code','high_school_major','batch_name','number']
if __name__ == '__main__':
    b = Batch()
    with open('batch_info.txt') as f:
        for l in f:
            data = {filed[i]: v.decode('utf-8') for i, v in enumerate(l.strip().split(','))}
            b.insert_into_table(data, 'batch')