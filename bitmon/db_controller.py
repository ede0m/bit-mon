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
	last_raw_data_keys = list(snapshots_keys[-1].keys())
	last_raw_data = list(last_raw_data_keys[-1])
	last = last_raw_data["last"]
	return last



def writeOut():
	with open(os.path.join(os.path.dirname(__file__),"db.json"),'w') as jsonFile:
		#print(json.dumps(db, indent=4, sort_keys=True))
		jsonFile.write(json.dumps(db, indent=4, sort_keys=True))
		print('written')

