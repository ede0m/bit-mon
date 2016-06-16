import time
import json
from time import localtime
import requests
import os
import sys
from decimal import *
from api_call import api_call

class Daylog(object):

	def __init__(self, exchange):
		self.exchange = exchange
		self.key = None
		self.secret = None
		self.d_high = 0
		self.d_low = 0
		#self.mx_spread = 0
		self.daily_range = 0

	def get_logs(self):
		return self.daily_logs

	
	def __get_api_data(self, exchange):			
		api = api_call()
		if self.exchange == 'COIN-BS':
			api.rk()
		
		return api.get_data(exchange)

	
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
		data = self.__get_api_data(self.exchange)
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

		#sample most recent price 50 times within 1 minutes
		while count <= 24:
			#update snap vars
			data = self.__get_api_data(self.exchange)
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

			total_last = total_last + last 
			
			print('-----------------')
			print('-  ' + str(buy_low) +'--BUY')
			print('-  ' + str(sell_high) + '--SELL')
			print('-  ' + str(spread) + '--SPREAD')
			print('-  ' + str(last) + '--LAST')

			time.sleep(ratio)
			count = count + 1 		

		# returns sample data from 30 sec with highest high, lowest low, and largest spread within the snapshot 

		return (mn_buy, mx_sell, (total_last/(count+1)))
	
	
	##########################################################################
	# Logs entire day of coin flux at freq of 2.5 mins when entry_count = 576
	##########################################################################
	def log_day(self):
		#Start logging for one day
		entry_count = 0
		curr_date = time.strftime("%Y-%m-%d", localtime())

		#create log file and directory
		path = 'bitmon/logs/'+ self.exchange +'/'+curr_date
		if not os.path.exists(path):
		   		os.makedirs(path)	
		
		#START EVERY DAY call ratios 
		if self.exchange == 'COIN-BS':
			adjust_ratio = 0.1
		elif self.exchange == 'BLK-CHN':
			adjust_ratio = 1.02 
		elif self.exchange == 'OKC':
			adjust_ratio = 1.00
	
		# 576 entries for a day 
		while entry_count <= 575: 
			
			filename = 'entry_' + str(entry_count) + '.txt'
			entry = open(os.path.join(path,filename), 'w')
			
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
		
			
			#5 snapshots = 2.5 minutes = 1 entry
			while count <= 3: 
				time_A = time.time()  
				snap = self.__snapshot(adjust_ratio)
				
				if not any(snap):
					print('\n\n-----ENTRY ERROR---- Snap returned None \n\n')
					success = False
					return 

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
			if success == False:
				entry.write('NON SUCCESSFUL ENTRY -- ERROR OCCURED on entry # ' + str(entry_count) +'\n')
						
			elif success == True:
				print('\n ENTRY ' + str(entry_count) + ' Written \n')
				e_range = e_high - e_low
				entry.write('ENTRY ' + str(entry_count) + ': \n')
				entry.write('--TIME: ' + time.strftime("%H:%M:%S", localtime()) + '\n')
				entry.write('--SELL-HIGH: ' + str(e_sell) + '\n')
				entry.write('--BUY-LOW: '  + str(e_buy) + '\n')
				entry.write('--SPREAD: '+ str(e_spread) + '\n')
				entry.write('--HIGH: '+ str(e_high) + '\n')
				entry.write('--LOW: '+ str(e_low) + '\n')
				entry.write('--RANGE: '+ str(e_range) +'\n----------------------------\n' )
				entry_count = entry_count + 1			
			
		

		# add to daily logs
		self.d_range = self.d_high - self.d_low
		self.daily_logs.append(( self.d_high, self.d_low, self.d_range))
		
		print (self.daily_logs) 
		
