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
	}		 

	# Returns profit ratio from best spread between any 2 markets
	def get_spread_info(self):
		best_buy = 0
		best_sell = 0
		exchange_buy = ''
		exchange_sell = ''


		bc_last = float(masterDBcontroller.getLast("COIN-BS"))
		krk_last = float(masterDBcontroller.getLast("KRK"))

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
			

		print(bc_last)
		print(krk_last)

		profit_r = (best_sell - best_buy) / best_buy
		res = (best_buy, best_sell, profit_r, exchange_buy, exchange_sell)
		print(res)
		return res


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

	# def makeTrade():
	# 	#sell('KRK', .01, 'BTC')

trader = Trader()
trader.get_spread_info()

