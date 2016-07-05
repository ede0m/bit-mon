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
		baseline = .5
		exchange_pair_list = {
		'exchanges': { 
		'COIN-BS/KRK' :	{
			'usd_balance_r':'',
			'last_trade': {
					'buy':	{
						'buyer':'',
						'price':''
					},
					'sell': {
						'seller':'',
						'price':''
							}
						}
					}
				}
		}




	def logTrade(buying_e, selling_e, date, time):
		masterDBcontroller.db["trades"][date] = {}
		masterDBcontroller.db["trades"][date][time] = {}
		masterDBcontroller.db["trades"][date][time]["sell_exchange"] = selling_e
		masterDBcontroller.db["trades"][date][time]["buy-exhange"] = buying_e


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


	def trade_decision():
		
		input_spread = self.__get_spread_info()
		buyingMKT_price = input_spread[0]
		sellingMKT_price = input_spread[1]
		spread = (sellingMKT_price - buyingMKT_price)
		spread_r = input_spread[2]
		ex_buy = input_spread[3]
		ex_sell = input_spread[4]
		exchange_pair = input_spread[5]
		
		total_assets = get_balance()
		self.usd_assets = total_assets[0] + total_assets[2]
		self.bc_assets = total_assets[1] + total_assets[3]
		worth_unit = ((best_buy + best_sell)/2)
		self.bc_worth = (self.usd_assets / worth_unit) + self.bc_assets
		self.usd_worth = (self.bc_assets * worth_unit) + self.usd_assets
		self.bc_r = self.bc_assets/self.bc_worth
		self.usd_r = self.usd_assets/self.usd_worth

		buyer_b = get_balance(exchange=ex_buy)
		seller_b = get_balance(exchange=ex_sell) 
		buyer_usd_b = buyer_b[0]
		buyer_bt_b = buyer_b[1]
		seller_usd_b = seller_b[0]
		seller_bt_b = seller_b[1]
		# OTHER EXCHANGE ASSET DATA
		ex_pair[ex_pair]['usd_balance_r'] == buyer_b / seller_b
		# OTHER EXCHANGE PAIRS

		# default trade is 6% of payable assets in any one market 
		volume = .00

		##################   MANAGE UNBALANCED ACCOUNTS   ##########################


		usd_balance_r = ex_pair[ex_pair]['usd_balance_r']
		# BUYINF EXCHANGE HAS MORE USD 
		if (usd_balance_r > 2.285):

			difference = buyer_b - seller_b
			amount_usd = difference / 2
			last_ex_buy = self.exchange_pair_list[ex_pair]['last_trade']['buy']['buyer']
			last_ex_sell = self.exchange_pair_list[ex_pair]['last_trade']['sell']['seller']
			last_buy_price = self.exchange_pair_list[ex_pair]['last_trade']['buy']['price']
			last_sell_price = self.exchange_pair_list[ex_pair]['last_trade']['sell']['price']
			# REVERSE TRADE TO EVEN OUT ACCOUTS, BITCH
			if ex_buy == last_ex_sell and ex_sell == last_ex_buy:
				print('Reverse Trade Started')
				# WARNING! THIS COULD MAKE HIGH VOLUME TRADES 
				amount = amount_usd/buyingMKT_price
				trade = makeTrade(ex_buy, ex_sell, amount, buyingMKT_price, sellingMKT_price)
				monthdayyear = time.strftime("%m/%d/%Y")
				t = time.strftime('%H-%M-%S')
				logTrade(ex_buy, ex_sell, trade, monthdayyear, t)
				return
			
			# BUYING MARKET HAS NOT CHANGED 
			# If exchange with more USD can buy BTC for below last trade buy price to even out accounts and make some moneyyy
			elif buyingMKT_price > last_sell_price: 
				amount = buyer_bt_b / 2
				sell = makeSell(ex_buy, amount)
				print('Buying Exchange Balance Evened')
				if sellingMKT_price < last_buy_price:
				 	amount = (seller_usd_b / 2) / sellingMKT_price
				 	buy = makeBuy(ex_sell, amount)
				 	print('Selling Exchange Balance Evened')
				 	return
				else:
					print('WARNING! Buying Exchange Balance UNEVEN!')
					return
			
			print('WARNING! Uneven Balance for this exchange pair not managed')	 	
			return
		
		
		# SELLING EXCHANGE HAS MORE USD
		elif (usd_balance_r < .35):

			difference = seller_b - buyer_b
			amount_usd = difference / 2
			last_ex_buy = self.exchange_pair_list[ex_pair]['last_trade']['buy']['buyer']
			last_ex_sell = self.exchange_pair_list[ex_pair]['last_trade']['sell']['seller']
			last_buy_price = self.exchange_pair_list[ex_pair]['last_trade']['buy']['price']
			last_sell_price = self.exchange_pair_list[ex_pair]['last_trade']['sell']['price']
			if ex_buy == last_ex_sell and ex_sell == last_ex_buy:
				print('Reverse Trade Started')
				# WARNING! THIS COULD MAKE HIGH VOLUME TRADES 
				amount = amount_usd/buyingMKT_price
				trade = makeTrade(ex_buy, ex_sell, amount, buyingMKT_price, sellingMKT_price)
				monthdayyear = time.strftime("%m/%d/%Y")
				t = time.strftime('%H-%M-%S')
				logTrade(ex_buy, ex_sell, trade, monthdayyear, t)
				return
			# SELLING MARKET HAS NOT CHANGED
			# If exchange with more USD can buy BTC for below last trade buy price to even out accounts and make some moneyyy
			elif sellingMKT_price < last_buy_price:
				amount = (seller_usd_b / 2) / sellingMKT_price
				buy = makeBuy(ex_sell, amount) 					# NOW SELLING EXCHANGE IS EVENED OUT
				print('Selling Exchange Balance Evened')
				#Check if buying exchange can be evened to fully even out pair of exchanges 
				if buyingMKT_price > last_sell_price:
					amount = buyer_bt_b / 2
					sell = makeSell(ex_buy, amount)
					print('Buying Exchange Balance Evened')
					return
				else:
					print('WARNING! Buying Exchange Balance UNEVEN!')
					return
			
			print('WARNING! Uneven Balance for this exchange pair not managed')	 	
			return


		####################################################################
		################        REGULAR PROCEDURE        ###################

		# we have more bitcoin than we should and spread looks GREAT. 
		if(self.bc_r > .4 and self.usd_assets > self.usd_base and spread_r > .016):
			volume = .40
			amount_usd = buyer_b * volume
			amount = amount_usd/buyingMKT_price
			trade = makeTrade(ex_buy, ex_sell, amount, buyingMKT_price, sellingMKT_price)
			monthdayyear = time.strftime("%m/%d/%Y")
			t = time.strftime('%H-%M-%S')
			logTrade(ex_buy, ex_sell, trade, monthdayyear, t)
			return
			  

		# probably some logic in here to determine how much we wanna buy
		if(self.bc_r > .25 and self.usd_assets > self.usd_base and spread_r > 0.01):
			volume = .20
			amount_usd = buyer_b * volume
			amount = amount_usd/buyingMKT_price
			trade = makeTrade(ex_buy, ex_sell, amount, buyingMKT_price, sellingMKT_price)
			monthdayyear = time.strftime("%m/%d/%Y")
			t = time.strftime('%H-%M-%S')
			logTrade(ex_buy, ex_sell, trade, monthdayyear, t)
			return
		
		# Same ol shit
		if(self.bc_r > .10 and self.usd_assets > self.usd_base and spread_r > 0.004):
			volume = .10
			amount_usd = buyer_b * volume
			amount = amount_usd/buyingMKT_price
			trade = makeTrade(ex_buy, ex_sell, amount, buyingMKT_price, sellingMKT_price)
			monthdayyear = time.strftime("%m/%d/%Y")
			t = time.strftime('%H-%M-%S')
			logTrade(ex_buy, ex_sell, trade, monthdayyear, t)
			return

		#####################################################################

	def makeTrade(buyer, seller, amount, buying_price, selling_price):

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
		if (spread - total_fee) < self.baseline:
			print('\n - - -  PROFIT LESS THAN BASELINE  - - -  \n - - -  TRADE ABORTED  - - - \n\n')
			return False
		# Make a trade and get rich
		else:
			self.exchange_pair_list[ex_pair]['last_trade']['buy']['buyer'] = buyer
			self.exchange_pair_list[ex_pair]['last_trade']['buy']['price'] = buying_price
			self.exchange_pair_list[ex_pair]['last_trade']['sell']['seller'] = seller
			self.exchange_pair_list[ex_pair]['last_trade']['sell']['price'] = selling_price

			buy = buy(buyer, amount, 'BTC')
			sell = sell(seller, amount, 'BTC')
			return selling_price - buying_price - buy_fee - sell_fee
			# MAY WANT TO QUERY ACTUAL DATA FROM BUY AND SELL to get final profit.



		#LOG STUFF TO DB

	def makeBuy(exchange, amount):

		buy(exchange, amount, 'BTC')

	def makeSell(exchange, amount):

		sell(exchange, amount, 'BTC')



trader = Trader()
trader.get_spread_info()