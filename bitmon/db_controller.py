import time
import json
import os

db = {}

with open(os.path.join(os.path.dirname(__file__),"db.json"),'r') as data_file:  
		global db  
		db = json.load(data_file)
		


def newMonthLog(exchange):
	global db
	monthyear = time.strftime("%m/%Y")
	db[exchange]['logs'][monthyear] = {}
	return monthyear

def newCurrDate(exchange, monthyear, snaps_logs, currdate):
		global db
		db[exchange][snaps_logs][monthyear][str(currdate)] = {}
		print(json.dumps(db, indent=4, sort_keys=True))


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


def writeOut():
	with open(os.path.join(os.path.dirname(__file__),"db.json"),'w') as jsonFile:
		print(json.dumps(db, indent=4, sort_keys=True))
		jsonFile.write(json.dumps(db, indent=4, sort_keys=True))
		print('written')

