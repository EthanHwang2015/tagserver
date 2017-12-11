#encoding=utf8
import io

labels = [u'物流',u'代办',u'运动',u'游戏',u'社交',u'出行',
    u'学习',u'维修',u'招聘',u'家教',u'信息咨询',u'租房',u'美容',
    u'宠物',u'各种无聊',u'代课点名',u'租借',u'求购',u'出租',u'出售']

print len(labels)
for label in sorted(labels):
    print label

keys = {}
with io.open('train.txt', 'r', encoding='utf-8') as f:
    for row in f:
        row = row.strip('\n')
        cols = row.split('\\t')
        if len(cols) == 2:
            key = cols[0].strip()
            if key in keys:
                keys[key] +=1
#                print "{}\t{}".format(key.encode('utf8'),cols[1].encode('utf8'))
            else:
                keys[key]=1

#                print "{}\t{}".format(key.encode('utf8'),cols[1].encode('utf8'))
        else:
            cols = row.split('/t')
            if len(cols) == 2:
                key = cols[0].strip()
                if key in keys:
                    keys[key]  +=1
#                    print "{}\t{}".format(key.encode('utf8'),cols[1].encode('utf8'))
                else:
                    keys[key]=1
#                    print "{}\t{}".format(key.encode('utf8'),cols[1].encode('utf8'))

print len(keys)
for key in sorted(keys.keys()):
    print key,keys[key]

