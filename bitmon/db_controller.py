import time
import json
import os



db = {}

with open(os.path.join(os.path.dirname(__file__),"db.json"),'r') as data_file:
    global db
        db = json.load(data_file)



def newDateLog(exchange, log_type):
    global db
        monthdayyear = time.strftime("%m/%d/%Y")
        db[exchange][log_type][monthdayyear] = {}


def getBLKLogs():
    logs = db['BLK_CHN']['logs']
        return logs

def getCOINBSLogs():
    logs = db['COIN_BS']['logs']
        return logs

def getOKCLogs():
    logs = db['OKC']['logs']
        return logs

def getBLKSnapshots():
    snaps = db['BLK_CHN']['snapshots']
        return snaps

def getCOINBSSnapshots():
    snaps = db['COIN_BS']['snapshots']
        return snaps

def getOKCSnapshots():
    snaps = db['OKC']['snapshots']
        return snaps

def getLastValue(exchange):
    snapshots_keys = list(db[exchange]['snapshots'].keys())
    last_key = snapshots_keys[0]
    # print(last_key)
    for key in snapshots_keys:   
        sp = key.split("/")[1]
            if(int(last_key.split('/')[1]) < int(sp)):
                last_key = key
    last_raw_data_keys = list(db[exchange]['snapshots'][last_key].keys())
    last_raw_data_key = last_raw_data_keys[0]
    for key in last_raw_data_keys:
        print("key ---> ", key)
        print("last_raw_data_key ----> ", last_raw_data_key)
        mn = key.split("-")[0]
        sc = key.split("-")[1]
        print("int(last_raw_data_key.split('-')[0]) <= int(mn) and int(last_raw_data_key.split('-')[1]) < int(sc) ------- ", int(last_raw_data_key.split('-')[0]) <= int(mn) and int(last_raw_data_key.split('-')[1]) < int(sc), int(last_raw_data_key.split('-')[0]), int(mn), int(last_raw_data_key.split('-')[1]),  int(sc))
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
        return last_num



def writeOut():
    with open(os.path.join(os.path.dirname(__file__),"db.json"),'w') as jsonFile:
        #print(json.dumps(db, indent=4, sort_keys=True))
        jsonFile.write(json.dumps(db, indent=4, sort_keys=True))
            print('written')

