#!/usr/bin/python3
import fileinput
import os
import time
from time import localtime
#import Daylog ##MAYBE


#class will run independently and consistently analyse data
class Lab_stat(object):
		
	def __init__(self, exchange):
		self.spreads = []
		self.exchange = exchange
		self.last_list = []
		self.price_list = []

	 ## NEED TO FIRGURE OUT A WAY TO RE-WRITE LOGS IN Daylog so I can continusouly update my spread_bound 
	def __parse_logs(self):
		count = 0
		log_date = time.strftime("%Y-%m-%d", localtime())
		#look through DAILY stats
		files = 0
		for file in os.listdir('logs/'+self.exchange+'/'+log_date+'/'):
			if file.endswith('.txt'):
				files = files + 1
	#	print(files)
		while count < files: 
			spread_data = [None] * 2
			time_data = [None] * 2
			last_data = [None] * 2
			filename = 'logs/'+ self.exchange +'/' + log_date + '/entry_'+ str(count) +'.txt'
			for line in fileinput.input(filename):
				#get time data
				if line[2] == 'T':
					time_data = line.split(' ')
					time_dr = time_data[1]
				#get spread data
				if line[2] == 'S' and line[3] == 'P':
					spread_data = line.split(' ')
					spread_dr = float(spread_data[1])
				#Get LAST/HIGH data 
				if line[2] == 'H':
					last_data = line.split(' ')
					last_dr = float(last_data[1]) 
				# THIS MAY NOT WORK.. 
				if os.stat(filename).st_size == 0:
					continue				

			self.last_list.append((last_dr, time_dr))
			self.price_list.append((last_dr, time_dr))
			self.spreads.append((spread_dr, time_dr ))
			count = count + 1				
			

	#returns an acceptable spread range (or yes or no buy decision) (to trade class) that adjusts based on how fast the average spread is increasing. Useful for comapring best buy and sell on a single market and/or capitalizing on market frenzies.   
	def BTC_watch(self):
<<<<<<< HEAD
		self.__parse_logs()
		add_last = 0

		for last in self.last_list:
			add_last = add_last + last[0]
			print(last[0]) 
		last_av = (add_last / len(self.last_list))
		print('LAST AV:')
		print(last_av)

	#Returns best transaction based on the current market status
	def cross_site_analysis():
		
		initiate = false
		transaction = (buying, selling)
		return (initiate, transaction)

	def profit_tracker():
		#listtransactions coinbase API

		increasing = 0
		delta_price = 0
		loop = 0
		while loop < 573:
			self.__parse_logs()
			add_curr = 0
			
			for price in self.price_list:
				add_curr = add_curr + price[0] 
			curr_av = (add_curr / len(self.price_list))		
			print(curr_av)
			delta_curr = self.price_list[(len(self.price_list)-1)][0] - self.price_list[len(self.price_list)-2][0]
			print('----- Current Price Change: ' + str(delta_curr) + '\n')			
			# handle price increases
			if delta_curr > 0:
				delta_price += delta_curr
				increasing += 1
			elif delta_curr > 10:
				print('----- POSSIBLE SWING UP -----') 
				
			# handle price decreases 
			if delta_curr < 0:
				delta_price -= delta_curr
				increasing -= 1
			elif delta_curr < -10:
				print('----- POSSIBLE SWING DOWN -----')
			
			# handle constant market movements
			if increasing == 4 and delta_price > 20:
				print('----- INCREASE HAS NOT STOPPED IN 10 MINUTES OR MORE -----')
				break
			elif increasing == -4 and delta_price < -20:
				print('----- DECREASE HAS NOT STOPPED IN 10 MINUTES OR MORE -----')
				break
		
			print('--INCREASING: '+ str(increasing) + ' times')
			print('-- SLEEPING --')
			time.sleep(150)
			print('-- WAKING UP --')
			loop += 1	
				



stat = Lab_stat('COIN-BS')
stat.BTC_watch()
