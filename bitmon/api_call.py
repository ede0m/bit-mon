#!/usr/bin/python3

from decimal import *
from coinbase.wallet.client import Client
import os
import fileinput
import sys
import requests
class api_call(object):

	def __init__(self):
		self.CB_key = None
		self.CB_secret = None

	def rk(self):
		where_s = os.getcwd()
		where_s = where_s.split('/')
		if where_s[len(where_s)-1] == 'bit-mon':
			where_s = os.getcwd()
	
		elif where_s[len(where_s)-1] == 'bitmon':
			os.chdir('..')
			where_s = os.getcwd()

		filename = where_s + '/KEYS.txt'
		key = ''
		secret = ''
		count = 0
		for line in fileinput.input(filename):
			# COINBASE KEY PARSING
			if line[0] == 'C' and line[1] == 'B':
				if line[4] == 'K':
					self.CB_key = line.split(' ')[1]
				elif line[4] == 'S':
					self.CB_secret = line.split(' ')[1]
				else:
					print('NO API KEY, sorry chump')


			# OTHER API KEY PARSING 
	#		if line[0] == 'B' and line[1] == 'K':
	#			if line[5] = 'K':
	#				key = line.split(' ')[1]
	#			elif line[5] = 'S':
	#				secret = line.split(' ')[1]
	#			else:
	#				print('NO API KEY, sorry chump')
							
		
		
				

	##########################
	# THX COINBASE! 
	##########################
	def get_data(self, exchange):
	
		buy = 0
		sell = 0
		last = 0
		
		try:
			if exchange == 'BLK-CHN':
				response = requests.get('https://blockchain.info/ticker')
				r = response.json() 	
				last = r["USD"]["last"]
				buy = r["USD"]["buy"]
				sell = r["USD"]["sell"]	
	
		
			elif exchange == 'COIN-BS':
				client = Client(self.CB_key, self.CB_secret)
				r = client.get_sell_price()
				sell = r["amount"]		
				r = client.get_buy_price()
				buy = r["amount"]
				r = client.get_spot_price()
				last = r["amount"]
							
			elif exchange == 'OKC':
				response = requests.get('https://www.okcoin.com/api/v1/ticker.do?symbol=ltc_usd')
				r = response.json()
				last = r["ticker"]["last"]
				buy = r["ticker"]["buy"]
				sell = r["ticker"]["sell"]

		except ValueError:
			print('\nValue Error: Request skipped\n')
			return				
				
		return (Decimal(buy).quantize(Decimal('.01')), Decimal(sell).quantize(Decimal('.01')), Decimal(last).quantize(Decimal('.01')))	
	
