import os, sys, json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_call import *


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
	}		 

	# Returns profit ratio from best spread between any 2 markets
	def __get_spread_info():
		best_buy = 0
		best_sell = 0
		exchange_buy = ''
		exchange_sell = ''

		with open(CB_db.json) as data_file:
			data = json.load(data_file)
		return (best_buy, best_sell, ((best_sell - best_buy) / best_buy), exchange_buy, exchange_sell)


	## UP FOR DISCUSSION ---> This are more of examples then code

	## This is supposed to sort of form a "filter" or "funnel" that 
	## our data falls down and determines risk vs. return kinda
	def trade_decision():
		
		input_spread = self.__get_spread_info()
		spread = (input_spread[1] - input_spread[0])
		spread_r = input_spread[2]
		total_assets = get_balance()
		print(total_assets)
		self.usd_assets = total_assets[0]
		self.bc_assets = total_assets[1]
		worth_unit = ((best_buy + best_sell)/2)
		self.bc_worth = (self.usd_assets / worth_unit) + self.bc_assets
		self.usd_worth = (self.bc_assets * worth_unit) + self.usd_assets
		self.bc_r = self.bc_assets/self.bc_worth
		self.usd_r = self.usd_assets/self.usd_worth



		buy = "" # variable controlling if we buy
		sell = "" # variable controlling if we sell
	
		# we have more bitcoin than we should and spread looks good. 
		if(bc_r > 4. and bc_assets >= bc_base and spread > .015):
			sell = "S"
		# we have more than 60% of our funds in USD, buy bitcoin
		if(usd_r > .6 and usd_assets >= usd_base and spread > .015):
			buy = "B"
		# probably some logic in here to determine how much we wanna buy
		if(bc_r > .2 and bc_r <= .4 and bc_assets > bc_base and spread > 0.025):
			sell = "S"
		# probs some logic shit
		if(usd_r > .2 and usd_r <= .4 and usd_assets > usd_base and spread > 0.025):
			buy = "B"
		# Same ol shit
		if(bc_r < .2 and bc_assets > usd_base and spread > 0.035):
			sell = "S"
		# Some shit maybe?
		if(usd_r < .2 and usd_assets > usd_base and spread > 0.035):
			buy = "B"
		# shit
		
		return sell + buy

	def makeTrade():
		#sell('KRK', .01, 'BTC')

trader = Trader()
trader.trade_decision()

