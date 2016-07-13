import os
import json
import DB.merger

db = {}

def load():
	## pulling in krk db to add to master db
	global db
	with open(os.path.join(os.path.dirname(__file__),"master_db.json"),'r') as data_file:
		db = json.load(data_file);

# def getSnaps():

# 	date.lower()
# 	if date == "all":
# 		keys = list(db[exchange]['snapshots'].keys())
# 		p_db = {}
# 		for key in keys:
# 			p_db[key] = db[exchange]['snapshots'][key]
			
# 		print(json.dumps(p_db, indent=4, sort_keys=True))


def getBestSpread():
    return db["best-spread"]["spread"]

def setBestSpread(new, date):
    db["best-spread"]["spread"] = new
    db["best-spread"]["date"] = date
    with open(os.path.join(os.path.dirname(__file__),"master_db.json"),'w') as data_file:
        data_file.write(json.dumps(db, indent=4, sort_keys=True))

def getLast(exchange):
    DB.merger.merge()
    load()
    # print(json.dumps(db, indent=4, sort_keys=True))
    snapshots_keys = list(db[exchange]['snapshots'].keys())
    last_key = snapshots_keys[0]
    for i in snapshots_keys:
    	tempkey = last_key.split('/')
    	temp = i.split("/")
    	if(temp[0] >= tempkey[0] and temp[1] > tempkey[1]):
    		last_key = i
    # print(snapshots_keys)
    
    # print(last_key)
    for key in snapshots_keys:   
        day = key.split("/")[1]
        month = key.split("/")[0]
        passover = False
        # print("int(last_key.split('/')[1]) < int(day) or int(last_key.split('/')[0]) < int(month)", (int(last_key.split('/')[1]) < int(day)), (int(last_key.split("/")[0]) < int(month)))
        # print(int(month), int(last_key.split("/")[0])
        if(int(last_key.split("/")[0]) < int(month)):
                # print("fuuck")
                last_key = key
                passover = True
        elif(int(last_key.split('/')[1]) < int(day) and int(last_key.split("/")[0]) == int(month)):
            # print("agg")
            last_key = key
    # print(last_key)
    last_raw_data_keys = list(db[exchange]['snapshots'][last_key].keys())
    last_raw_data_key = last_raw_data_keys[0]
    for key in last_raw_data_keys:
        # print("key ---> ", key)
        # print("last_raw_data_key ----> ", last_raw_data_key)
        hr = key.split("-")[0]
        #print("int(last_raw_data_key.split('-')[0]) <= int(mn) and int(last_raw_data_key.split('-')[1]) < int(sc) ------- ", int(last_raw_data_key.split('-')[0]) <= int(mn) and int(last_raw_data_key.split('-')[1]) < int(sc), int(last_raw_data_key.split('-')[0]), int(mn), int(last_raw_data_key.split('-')[1]),  int(sc))
        if(int(last_raw_data_key.split('-')[0]) <= int(hr)):
            last_raw_data_key = key
            for ky in last_raw_data_keys:
                hor = ky.split("-")[0]
                minu = ky.split("-")[1]
                if (int(last_raw_data_key.split('-')[0]) <= int(hor) and int(last_raw_data_key.split('-')[1]) <= int(minu)):
                    last_raw_data_key = ky
                    for k in last_raw_data_keys:
                        h = k.split("-")[0]
                        m = k.split("-")[1]
                        s = k.split("-")[2]
                        if(int(last_raw_data_key.split('-')[0]) <= int(h) and int(last_raw_data_key.split('-')[1]) <= int(m) and int(last_raw_data_key.split('-')[2]) < int(s)):
                            last_raw_data_key = k
    # print(last_raw_data_key)
    last_raw_data = db[exchange]['snapshots'][last_key][last_raw_data_key]
    # print(last_raw_data)
    # print(last_raw_data)
    last = last_raw_data["last"]
    last_split = last.split("--")
    last_num = last_split[0]
    # print(last_num)
    res = (float(last_num), last_raw_data_key, last_key, exchange)
    return res


load()



	
