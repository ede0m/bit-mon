# from .bitmon.api_call import *
import sys
import os
import json
sys.path.append("..")
import masterDBcontroller


class Trader(object):

	def __init__(self):
		bc_assets = 0 # this is the current bitcoin balance accross the three markets?
		usd_assets = 0 # this is the current us dollar balance accross the three markets?
		bc_worth = 1 # TOTAL ASSETS (BTC and USD across all markets) represented in BTC
		usd_worth = 1 # # TOTAL ASSETS (BTC and USD across all markets) represented in USD
		bc_base = .1 # baseline for bc
		usd_base = 50 # baseline for us dollars
		bc_r = 0 # percentage of our net worth that is liquid bitcoin
		usd_r = 0 # percentage of our net worth that is liquid us dollars
		last_trade = None
		exchange_pair_list = [{'exchanges':'COIN-BS/KRK','usd_balance_r':'','last_trade':{'buy':{'buyer':'','price':''},'sell':{'seller':'','price':''}}}



								]

 

	# Returns profit ratio from best spread between any 2 markets
	def get_spread_info(self):
		lasts = []
		
		# GET ALL LAST INFO FROM EACH EXCHANGE
		lasts.append(masterDBcontroller.getLast('COIN-BS'))
		lasts.append(masterDBcontroller.getLast("KRK"))

		# why only kraken exchange??
		date = masterDBcontroller.getLast('KRK')[2]

		ex_buy = ''
		ex_sell = ''
		ex_pair = ''
		my_buy = lasts[0][0]
		my_sell = lasts[0][0]
		for last_val in lasts:
			if last_val[0] <= my_buy:
				my_buy = last_val[0]
				ex_buy = last_val[3]
			if last_val[0] >= my_sell:
				my_sell = last_val[0]
				ex_sell = last_val[3]

		if (ex_buy == 'COIN-BS' or ex_buy == 'KRK') and (ex_sell == 'COIN-BS' or ex_sell == 'KRK'):
			ex_pair = 'COIN-BS/KRK'


		profit_r = ((my_sell - my_buy) / my_buy)
		
		temp_best_spread = masterDBcontroller.getBestSpread()
		# what is this for?
		if(profit_r >= temp_best_spread):
			masterDBcontroller.setBestSpread(profit_r, date)
		res = (my_buy, my_sell, profit_r, ex_buy, ex_sell, ex_pair)
		print(res)
		return res


	## UP FOR DISCUSSION ---> This are more of examples then code

	## This is supposed to sort of form a "filter" or "funnel" that 
	## our data falls down and determines risk vs. return kinda
	def trade_decision():
		
		input_spread = self.__get_spread_info()
		buying_price = input_spread[0]
		selling_price = input_spread[1]
		spread = (selling_price - buying_price)
		spread_r = input_spread[2]
		exchange_pair = input_spread[5]
		
		total_assets = get_balance()
		print(total_assets)
		self.usd_assets = total_assets[0] + total_assets[2]
		self.bc_assets = total_assets[1] + total_assets[3]
		worth_unit = ((best_buy + best_sell)/2)
		self.bc_worth = (self.usd_assets / worth_unit) + self.bc_assets
		self.usd_worth = (self.bc_assets * worth_unit) + self.usd_assets
		self.bc_r = self.bc_assets/self.bc_worth
		self.usd_r = self.usd_assets/self.usd_worth

		KR_usd = total_assets[0]
		CB_usd = total_assets[2]
		KR_bt = total_assets[1]
		CB_bt = total_assets[3]
		# OTHER EXCHANGE ASSET DATA
		
		for ex_pair in self.exchange_pair_list:
			if ex_pair['exchanges'] == 'COIN-BS/KRK':
				ex_pair['usd_balance_r'] = CB_usd / KR_usd
			# OTHER EXCHANGE PAIRS



		ex_buy = input_spread[3]
		ex_sell = input_spread[4]

		# default trade is 6% of payable assets in any one market 
		volume = .00
		# baseline is the least amout of profit (in USD) accepted for a trade
		baseline =.25															# Maybe make a member var of the class

		##################   IF UNBALANCED ACCOUNTS   ##########################
		for ex_pair in self.exchange_pair_list:


			usd_balance_r = ex_pair['usd_balance_r']
			# Coin Base has more USD 
			if (usd_balance_r > 2.285):

				difference = CB_usd - KR_usd
				amount_usd = difference / 2
				# REVERSE TRADE TO EVEN OUT ACCOUTS, BITCH
				
				### TODO: MAKE LAST TRADE DYNAMIC TO THE PAIR_DICT
				if ex_buy == self.last_trade[1] and ex_sell == self.last_trade[0]:
					
					# WARNING! THIS COULD MAKE HIGH VOLUME TRADES 
					amount = amount_usd/buying_price
					self.last_trade(ex_buy, ex_sell, buying_price, selling_price)
					trade = makeTrade(ex_buy, ex_sell, amount, buying_price, selling_price, baseline)
					return
				
				
			# KRK has more USD
			elif (usd_balance_r < .35):

				difference = KR_usd - CB_usd
				amount_usd = difference / 2
				if ex_buy == self.last_trade[1] and ex_sell == self.last_trade[0]:
					
					# WARNING! THIS COULD MAKE HIGH VOLUME TRADES 
					amount = amount_usd/buying_price
					self.last_trade(ex_buy, ex_sell, buying_price, selling_price)
					trade = makeTrade(ex_buy, ex_sell, amount, buying_price, selling_price, baseline)
					return

		####################################################################


		# we have more bitcoin than we should and spread looks GREAT. 
		if(self.bc_r > .4 and self.usd_assets > self.usd_base and spread_r > .016):
			volume = .40
			amount_usd = KR_usd * volume
			amount = amount_usd/buying_price
			self.last_trade = (ex_buy, ex_sell, buying_price, selling_price)
			trade = makeTrade(ex_buy, ex_sell, amount, buying_price, selling_price, baseline)
			return
			  

		# probably some logic in here to determine how much we wanna buy
		if(self.bc_r > .25 and self.usd_assets > self.usd_base and spread_r > 0.01):
			volume = .20
			amount_usd = KR_usd * volume
			amount = amount_usd/buying_price
			self.last_trade = (ex_buy, ex_sell, buying_price, selling_price)
			trade = makeTrade(ex_buy, ex_sell, amount, buying_price, selling_price, baseline)
			return
		
		# Same ol shit
		if(self.bc_r > .10 and self.usd_assets > self.usd_base and spread_r > 0.004):
			volume = .10
			amount_usd = KR_usd * volume
			amount = amount_usd/buying_price
			self.last_trade = (ex_buy, ex_sell, buying_price, selling_price)
			trade = makeTrade(ex_buy, ex_sell, amount, buying_price, selling_price, baseline)
			return

	# def makeTrade():
	# 	#sell('KRK', .01, 'BTC')
	def makeTrade(buyer, seller, amount, buying_price, selling_price, baseline):
		
		#CHECK FEES AGAINST profit
		# coinbase has a buy / sell fee of 1%
		spread = selling_price - buying_price	

		if buyer == 'COIN-BS':
			buy_fee = float("{0:.2f}".format((.01)(buying_price)(amount)))
		# kraken changes fee based on volume of trades per user. Will always be between 0.16% and 0.26%
		if buyer == 'KRK':
			buy_fee = float("{0:.2f}".format((.0016)(buying_price)(amount)))
		
		if seller == 'COIN-BS':
			sell_fee = float("{0:.2f}".format((.01)(selling_price)(amount)))
		
		if seller == 'KRK':
			sell_fee = float("{0:.2f}".format((.0016)(selling_price)(amount)))

		total_fee = buy_fee + sell_fee

		# Never make a trade that profits less than 25 cents
		if (spread - total_fee) < baseline:
			print('\n - - -  PROFIT LESS THAN BASELINE  - - -  \n - - -  TRADE ABORTED  - - - \n\n')
			return False
		# Make a trade and get rich
		else:
			buy = buy(buyer, amount, 'BTC')
			sell = sell(seller, amount, 'BTC')

			# MAY WANT TO QUERY ACTUAL DATA FROM BUY AND SELL to get final profit.




		#LOG STUFF TO DB

	def makeBuy(exchange, amount):

		buy(exchange, amount, 'BTC')

	def makeSell(exchange, amount):

		sell(exchange, amount, 'BTC')


trade = Trader()
trade.get_spread_info()