import time
import json
import os



db = {}


def initialize(exchange):
    if exchange == "COIN-BS":
        with open(os.path.join(os.path.dirname(__file__),"CB_db.json"),'r') as data_file:
            global db
            db = json.load(data_file)
    elif exchange == "KRK":
        with open(os.path.join(os.path.dirname(__file__),"KN_db.json"),'r') as data_file:
            global db
            db = json.load(data_file)
    elif exchange == 'ITBT':
        with open(os.path.join(os.path.dirname(__file__),"ITBT_db.json"),'r') as data_file:
            global db
            db = json.load(data_file)




def newDateLog(log_type):
    global db
    monthdayyear = time.strftime("%m/%d/%Y")
    db[log_type][monthdayyear] = {}


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


def writeOut(exchange):
    global db
    if exchange == "COIN-BS":
        with open(os.path.join(os.path.dirname(__file__),"CB_db.json"),'w') as data_file:
            data_file.write(json.dumps(db, indent=4, sort_keys=True))
            print('written')
    elif exchange == "KRK":
        with open(os.path.join(os.path.dirname(__file__),"KN_db.json"),'w') as data_file:
            data_file.write(json.dumps(db, indent=4, sort_keys=True))
            print('written')
    elif exchange == "ITBT":
        with open(os.path.join(os.path.dirname(__file__),"ITBT_db.json"),'w') as data_file:
            data_file.write(json.dumps(db, indent=4, sort_keys=True))
            print('written')



    # with open(os.path.join(os.path.dirname(__file__),"db.json"),'w') as jsonFile:
    #     #print(json.dumps(db, indent=4, sort_keys=True))
    #     jsonFile.write(json.dumps(db, indent=4, sort_keys=True))
    #     print('written')

