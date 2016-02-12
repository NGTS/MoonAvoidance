import numpy as np
import pymysql
db=pymysql.connect(host='ngtsdb',db='ngts_ops')
f=open('pre_baffle_imglist.txt','r').readlines()
img,action_id=[],[]
for i in f:
	img.append(i.split('\n')[0])
f.close()
for i in img:
	qry="SELECT action_id FROM raw_image_list WHERE image_id=%s LIMIT 1" % i
	with db.cursor() as cur:
		cur.execute(qry)	
		for row in cur:
			action_id.append(row[0])
print set(action_id)