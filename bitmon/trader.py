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
		bc_base = 0 # baseline for bc
		usd_base = 0 # baseline for us dollars
		bc_r = 0 # percentage of our net worth that is liquid bitcoin
		usd_r = 0 # percentage of our net worth that is liquid us dollars



	# MAYBE MOVE THIS TO MAIN, call return from Trader.trade_decision()
	# a combination of buy and sell can determine if we trade (do both) 
	initiateTrade = {
		"S" : "", # sell shit
		"B" : "", # buy shit
		"SB" : "" # TRADE shit
		"T" : "" # transfer
	}		 

	# Returns profit ratio from best spread between any 2 markets
	def get_spread_info(self):
		best_buy = 0
		best_sell = 0
		exchange_buy = ''
		exchange_sell = ''


		bc_last = float(masterDBcontroller.getLast("COIN-BS")[0])
		krk_last = float(masterDBcontroller.getLast("KRK")[0])

		date = masterDBcontroller.getLast("KRK")[2]

		if (bc_last - krk_last) < 0 :
			exchange_buy = "COIN-BS"
			best_buy = bc_last
			exchange_sell = "KRK"
			best_sell = krk_last
		else:
			exchange_buy = "KRK"
			best_buy = krk_last
			exchange_sell = "COIN-BS"
			best_sell = bc_last
			

		# print(bc_last)
		# print(krk_last)

		profit_r = (best_sell - best_buy) / best_buy
		res = (best_buy, best_sell, profit_r, exchange_buy, exchange_sell)
		print(res)
		temp_best_spread = masterDBcontroller.getBestSpread()
		if(profit_r >= temp_best_spread):
			masterDBcontroller.setBestSpread(profit_r, date)
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

		ex_buy = input_spread[3]
		ex_sell = input_spread[4]

		buy = "" # variable controlling if we buy
		sell = "" # variable controlling if we sell

		# default trade is 6% of payable assets in any one market 
		volume = .06
		# baseline is the least amout of profit (in USD) accepted for a trade
		baseline =.25


		# we have more bitcoin than we should and spread looks GREAT. 
		if(bc_r > .4 and bc_assets >= bc_base and spread_r > .016):
			volume = .40
			amount_usd = KR_usd * volume
			amount = amount_usd/buying_price
			trade = makeTrade(ex_buy, ex_sell, amount, buying_price, selling_price, baseline)

		# # we have more than 60% of our funds in USD, buy bitcoin
		# if(usd_r > .6 and usd_assets >= usd_base and spread_r > .015):
			  

		# probably some logic in here to determine how much we wanna buy
		if(bc_r > .25 and bc_assets > bc_base and spread_r > 0.01):
			volume = .20
			amount_usd = KR_usd * volume
			amount = amount_usd/buying_price
			trade = makeTrade(ex_buy, ex_sell, amount, buying_price, selling_price, baseline)
		
		# # probs some logic shit
		# if(usd_r > .2 and usd_r <= .4 and usd_assets > usd_base and buying_price, selling_price > 0.025):
		# 	buy = "B"
		
		# Same ol shit
		if(bc_r > .10 and bc_assets > usd_base and spread_r > 0.004):
			volume = .10
			amount_usd = KR_usd * volume
			amount = amount_usd/buying_price
			trade = makeTrade(ex_buy, ex_sell, amount, buying_price, selling_price, baseline)

		
		# # Some shit maybe?
		# if(usd_r < .2 and usd_assets > usd_base and spread > 0.035):
		# 	buy = "B"
		# # shit
		
		return sell + buy

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

