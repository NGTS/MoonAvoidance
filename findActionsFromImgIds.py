import numpy as np
import pymysql
db=pymysql.connect(host='ngtsdb',db='ngts_ops')
img=np.loadtxt('pre_baffle_imglist.txt',usecols=[0],unpack=True)
action_id=[]
for i in img:
	qry="SELECT action_id FROM raw_image_list WHERE image_id=%d LIMIT 1" % img
	with db.cursor() as cur:
		cr.execute(qry)	
		for row in cur:
			action_id.append(row[0])
print set(action_id)