#!/usr/bin/python3
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_call import *
import time
import json
from time import localtime
import requests
import db_controller
from decimal import *



class Daylog(object):

	def __init__(self, exchange):
		self.exchange = exchange
		self.d_high = 0
		self.d_low = 0
		self.daily_range = 0
		db_controller.initialize(self.exchange)

	def get_logs(self):
		return self.daily_logs

	
	def adjust_server_call(self, time_A, time_B, old):
		delta_time = time_B - time_A
		new = old
		# may have to adujust delta_time conditions based on frequency of snapshot
		if delta_time > 31 or delta_time < 29:						
			print('\n------ ADJUSTING CALL RATIO ------ \n')
			print('-----OLD: ' + str(old))
			c1 = 30 * old
			new = (c1 / delta_time)
			print('\n-----NEW: ' + str(new)) 
		print('\n------ SNAP FINISHED -------------\n')
		print('-----SEC: ' + str(delta_time) + '\n\n')		
		return new
	
	
	#############################################################################################
	# MEASURES 30 sec OF CURRENCY DATA WITH COUNT = 24 
	#############################################################################################


	def __snapshot(self, ratio):
		data = get_data(self.exchange)
		count = 0
		curr = 0
		sell_high = data[1]
		buy_low = data[0]
		mx_sell = sell_high
		mn_buy = buy_low
		spread = sell_high - buy_low
		mx_spread = spread
		last = data[2]
		total_last = last

		monthdayyear = time.strftime("%m/%d/%Y")

		#sample most recent price 25 times within 1/2 minutes
		while count <= 24:
			#update snap vars
			data = get_data(self.exchange)
			sell_high = data[1]
			buy_low = data[0]
			spread = data[1] - data[0]
			last = data[2]
			
			#Update snapshot return vars 
			if sell_high > mx_sell:
				mx_sell = sell_high
			elif buy_low < mn_buy:
				mn_buy = buy_low
			
			#Update daily high low data
			if self.d_high < last:
				self.d_high = last
			elif self.d_low > last:
				self.d_low = last
 
			
			print('-----------------')
			print('-  ' + str(buy_low) +'--BUY')
			print('-  ' + str(sell_high) + '--SELL')
			print('-  ' + str(spread) + '--SPREAD')
			print('-  ' + str(last) + '--LAST')


			time.sleep(ratio)
			count = count + 1 		

		# returns sample data from 30 sec with highest high, lowest low, and largest spread within the snapshot 		
		if monthdayyear not in db_controller.db['snapshots']:
			db_controller.newDateLog('snapshots')
		t = time.strftime('%M-%S')
		db_controller.db['snapshots'][monthdayyear][t] = {}
		db_controller.db['snapshots'][monthdayyear][t]['buy'] = str(mn_buy) +'--BUY\n'
		db_controller.db['snapshots'][monthdayyear][t]['sell'] = str(mx_sell) + '--SELL\n'
		db_controller.db['snapshots'][monthdayyear][t]['spread'] = str(spread) + '--SPREAD\n'
		db_controller.db['snapshots'][monthdayyear][t]['last'] = str(last) + '--LAST\n'
		db_controller.writeOut(self.exchange)
		return (mn_buy, mx_sell, last)
	
	
	##########################################################################
	# Logs entire day of coin flux at freq of 2.5 mins when entry_count = 576
	##########################################################################
	def log_day(self):

		#Create new DB keys if needed
		entry_count = 0
		curr_date = time.strftime("%m/%d/%Y")
		# =
		if curr_date not in (db_controller.db['logs']):
			db_controller.newDateLog('logs')

		
		#START EVERY DAY call ratios 
		if self.exchange == 'COIN-BS':
			adjust_ratio = 0.1
		elif self.exchange == 'BLK-CHN':
			adjust_ratio = 1.02 
		elif self.exchange == 'OKC':
			adjust_ratio = 1.00
		elif self.exchange == 'KRK':
			adjust_ratio = 1.00
	
		# 576 entries for a day 
		while entry_count <= 575: 
			
			entryname = 'entry_' + str(entry_count)
			
			#SAMPLE SNAP ---- CAUSES SLOW START Possibly 			
			time_a = time.time()
			print('\n------------------- STARTING ENTRY SAMPLE SNAP -------------------- \n')
			start_snap = self.__snapshot(adjust_ratio)
			time_b = time.time()
			adjust_ratio = self.adjust_server_call(time_a, time_b, adjust_ratio) ###### WILL ADJUST_RAT CHANGE BEFORE ASSIGNMENT?
			print('\n------------------- ENDING ENTRY SAMPLE SNAP ---------------------- \n\n')
			
			count = 0
			e_sell = start_snap[1]
			e_buy = start_snap[0]
			e_spread = e_sell - e_buy
			e_high = start_snap[2]
			e_low = start_snap[2]
			success = True
		
			
			# 10 snapshots = 5 minutes = 1 entry
			while count <= 8: 
				time_A = time.time()  
				snap = self.__snapshot(adjust_ratio)
				
				if not any(snap):
					print('\n\n-----ENTRY ERROR---- Snap returned None \n\n')
					success = False
					break

				sell = snap[1]
				st_sell = str(sell)
				buy = snap[0]
				st_buy = str(buy)
				spread = sell - buy
				st_spread = str(spread)
				last = snap[2]
				st_last = str(last)

				#Show Stats by 30sec
				print( '\n \n-----------------------------\nCOUNT ' + str(count) + ': \n--------\n' + '--TIME: '+\
				time.strftime("%H:%M:%S", localtime()) + '\n' +'--SELL-HIGH: ' + st_sell + '\n' +'--BUY-LOW: '  + \
				st_buy + '\n' + '--SPREAD: ' + st_spread  + '\n' + \
				'--LAST: ' + st_last + '\n----------------------------- \n')
			
				# update Entry vars
				if e_sell < sell:
					e_sell = sell
				elif e_buy > buy:
					e_buy = buy
				elif e_spread < spread:
					e_spread = spread
				elif last < e_low:
					e_low = last
				elif last > e_high:
					e_high = last
				count = count + 1
				
				# Adjust snap ratio
				time_B = time.time()
				adjust_ratio = self.adjust_server_call(time_A, time_B, adjust_ratio)				
			
			# MAKE LOG ENTRY 
			#db.newCurrDate(self.exchange, monthyear, 'logs', curr_date)

			if success == False:
				print('ENTRY WRITE FAILURE')
				db_controller.db[self.exchange]['logs'][curr_date]['entry'] = "entry " + str(entry_count) + "FAILURE BITCH \n"
			
			elif success == True:
				print('\n ENTRY ' + str(entry_count) + ' Written \n')
				t = time.strftime('%H-%M-%S')
				e_range = e_high - e_low
				db_controller.newDateLog('logs')
				db_controller.db['logs'][curr_date][t] = {}
				db_controller.db['logs'][curr_date][t]['entry'] = "entry " + str(entry_count) + "\n"
				db_controller.db['logs'][curr_date][t]['time'] = "time " + time.strftime("%H:%M:%S", localtime()) + "\n"
				db_controller.db['logs'][curr_date][t]['sell_high'] = "sell high: " + str(e_sell) + "\n"
				db_controller.db['logs'][curr_date][t]['buy_low'] = "buy low: " + str(e_buy) + "\n"
				db_controller.db['logs'][curr_date][t]['spread'] = "spread: " + str(e_spread) + "\n"
				db_controller.db['logs'][curr_date][t]['high'] = "high: " + str(e_high) + "\n"
				db_controller.db['logs'][curr_date][t]['low'] = "low: " + str(e_low) + "\n"
				db_controller.db['logs'][curr_date][t]['range'] = "range: " + str(e_range) + "\n"

				db_controller.writeOut(self.exchange)
				entry_count = entry_count + 1			
			
		

		# add to daily logs
		self.d_range = self.d_high - self.d_low
		self.daily_logs.append(( self.d_high, self.d_low, self.d_range))
	
