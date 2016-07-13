import os
import json

db = {}

def merge():
	## pulling in krk db to add to master db
	global db
	with open(os.path.join(os.path.dirname(__file__),"master_db.json"),'r') as data_file:
		db = json.load(data_file);
	with open(os.path.join(os.path.dirname("/Users/garritt/CODEDOG/bitcoin/bit-mon/bitmon/db/"),"KN_db.json"),'r') as data_file:
		KN_temp = json.load(data_file)
		# print(json.dumps(CB_temp, indent=4, sort_keys=True))
		KN_keys = list(KN_temp.keys())
		for key in KN_keys:
			# print(db)
			temp_keys = list(KN_temp[key].keys())
			# print(temp_keys)
			for date in temp_keys:
				if date not in db["KRK"][key] and key == "snapshots":
					temp_log_keys = list(KN_temp[key][date].keys())
					db["KRK"][key][date] = KN_temp[key][date]
					# print(temp_log_keys)
					for time in temp_log_keys:
						if time not in db["KRK"][key][date]:
							db['KRK'][key][date][time] = KN_temp[key][date][time]
				elif date in db["KRK"][key] and key == "snapshots":
					snap = list(KN_temp[key][date].keys())
					for time in snap:
							if time not in db["KRK"][key][date]:
								db['KRK'][key][date][time] = KN_temp[key][date][time]

				if date not in db["KRK"][key] and key == "logs":
						log = list(KN_temp[key][date].keys())
						db["KRK"][key][date] = KN_temp[key][date]
						for time in log:
							if time not in db["KRK"][key][date]:
								db['KRK'][key][date][time] = KN_temp[key][date][time]
				elif date in db["KRK"][key] and key == "logs":
					log = list(KN_temp[key][date].keys())
					for time in log:
							if time not in db["KRK"][key][date]:
								db['KRK'][key][date][time] = KN_temp[key][date][time]

	with open(os.path.join(os.path.dirname("/Users/garritt/CODEDOG/bitcoin/bit-mon/bitmon/db/"),"CB_db.json"),'r') as data_file:
		CB_temp = json.load(data_file)
		# print(json.dumps(CB_temp, indent=4, sort_keys=True))
		CB_keys = list(CB_temp.keys())
		for key in CB_keys:
			# print(db)
			temp_keys = list(CB_temp[key].keys())
			# print(temp_keys)
			for date in temp_keys:
				if date not in db["COIN-BS"][key] and key == "snapshots":
					snap = list(CB_temp[key][date].keys())
					db["COIN-BS"][key][date] = CB_temp[key][date]
					# print(temp_log_keys)
					for time in snap:
						if time not in db["COIN-BS"][key][date]:
							db['COIN-BS'][key][date][time] = CB_temp[key][date][time]
				elif date in db["COIN-BS"][key] and key == "snapshots":
					snap = list(CB_temp[key][date].keys())
					for time in snap:
						if time not in db["COIN-BS"][key][date]:
							db['COIN-BS'][key][date][time] = CB_temp[key][date][time]

				if date not in db["COIN-BS"][key] and key == "logs":
					log = list(CB_temp[key][date].keys())
					db["COIN-BS"][key][date] = CB_temp[key][date]
						# print(temp_log_keys)
					for time in log:
						if time not in db["COIN-BS"][key][date]:
							db['COIN-BS'][key][date][time] = CB_temp[key][date][time]
				elif date in db["COIN-BS"][key] and key == "logs":
					log = list(CB_temp[key][date].keys())
					for time in log:
							if time not in db["COIN-BS"][key][date]:
								db['COIN-BS'][key][date][time] = CB_temp[key][date][time]

					
	with open(os.path.join(os.path.dirname(__file__),"master_db.json"),'w') as data_file:
            data_file.write(json.dumps(db, indent=4, sort_keys=True))

merge()