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


load()
getSnaps("KRK")


	