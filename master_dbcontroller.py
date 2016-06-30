import os
import json

db = {}

def load():
	## pulling in krk db to add to master db
	global db
	with open(os.path.join(os.path.dirname(__file__),"master_db.json"),'r') as data_file:
		db = json.load(data_file);

def getSnaps():
	date = input("Which dates would you like?  ")
	date.lower()
	if date == "all":
		keys = list(db[exchange]['snapshots'].keys())
		p_db = {}
		for key in keys:
			p_db[key] = db[exchange]['snapshots'][key]
			
		print(json.dumps(p_db, indent=4, sort_keys=True))


def getLast(exchange):
    snapshots_keys = list(db[exchange]['snapshots'].keys())
    last_key = snapshots_keys[0]
    for i in snapshots_keys:
    	tempkey = last_key.split('/')
    	temp = i.split("/")
    	if(temp[0] >= tempkey[0] and temp[1] > tempkey[1]):
    		last_key = i
    print(snapshots_keys)
    
    print(last_key)
    for key in snapshots_keys:   
        sp = key.split("/")[1]
        if(int(last_key.split('/')[1]) < int(sp)):
            last_ky = key
    last_raw_data_keys = list(db[exchange]['snapshots'][last_key].keys())
    last_raw_data_key = last_raw_data_keys[0]
    for key in last_raw_data_keys:
        #print("key ---> ", key)
        #print("last_raw_data_key ----> ", last_raw_data_key)
        mn = key.split("-")[0]
        sc = key.split("-")[1]
        #print("int(last_raw_data_key.split('-')[0]) <= int(mn) and int(last_raw_data_key.split('-')[1]) < int(sc) ------- ", int(last_raw_data_key.split('-')[0]) <= int(mn) and int(last_raw_data_key.split('-')[1]) < int(sc), int(last_raw_data_key.split('-')[0]), int(mn), int(last_raw_data_key.split('-')[1]),  int(sc))
        if(int(last_raw_data_key.split('-')[0]) <= int(mn)):
            last_raw_data_key = key
            for ky in last_raw_data_keys:
                minu = ky.split("-")[0]
                sec = ky.split("-")[1]
                if (int(last_raw_data_key.split('-')[0]) <= int(minu) and int(last_raw_data_key.split('-')[1]) < int(sec)):
                    last_raw_data_key = ky
    # print(last_raw_data_key)
    last_raw_data = db[exchange]['snapshots'][last_key][last_raw_data_key]
    # print(last_raw_data)
    last = last_raw_data["last"]
    last_split = last.split("--")
    last_num = last_split[0]
    print(last_num)
    return last_num


load()
getLast("KRK")


	