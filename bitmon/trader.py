import sys, os
from api_call import *
import json
import DB.masterDBcontroller
import time
from decimal import *
from pymongo import MongoClient


class Trader(object):

	def __init__(self):
		self.bc_assets = 0 # this is the current bitcoin balance accross the three markets?
		self.usd_assets = 0 # this is the current us dollar balance accross the three markets?
		self.bc_worth = 1 # TOTAL ASSETS (BTC and USD across all markets) represented in BTC
		self.usd_worth = 1 # # TOTAL ASSETS (BTC and USD across all markets) represented in USD
		self.bc_base = .1 # baseline for bc
		self.usd_base = 10 # baseline for us dollars
		self.bc_r = 0 # percentage of our net worth that is liquid bitcoin
		self.usd_r = 0 # percentage of our net worth that is liquid us dollars
		self.baseline = .5
		
		# IMPLEMENT LOADING LAST_TRADE FROM DB.

		self.ex_dic = {
		'COIN-BS/KRK' :	{
			'usd_balance_r': None,
			'last_trade': {
					'buy':	{
						'buyer':'',
						'price': None
					},
					'sell': {
						'seller':'',
						'price': None
							}
					}
			},
		'ITBT/KRK': {
			'usd_balance_r': None,
			'last_trade': {
					'buy':	{
						'buyer':'',
						'price': None
					},
					'sell': {
						'seller':'',
						'price': None
							}
					}
			},
		'COIN-BS/ITBT': {
			'usd_balance_r': None,
			'last_trade': {
					'buy':	{
						'buyer':'',
						'price': None
					},
					'sell': {
						'seller':'',
						'price': None
							}
					}
			}
		}
	
	def __logTrade(self, buying_e, selling_e, buy_p, sell_p, fee):
		date = time.strftime("%m/%d/%Y")
		t = time.strftime('%H-%M-%S')
		profit = sell_p - buy_p - fee
		DB.masterDBcontroller.db["trades"][date] = {}
		DB.masterDBcontroller.db["trades"][date][t] = {}
		DB.masterDBcontroller.db["trades"][date][t]["sell-exchange"] = selling_e
		DB.masterDBcontroller.db["trades"][date][t]["buy-exhange"] = buying_e
		DB.masterDBcontroller.db["trades"][date][t]["buy-price"] = buy_p
		DB.masterDBcontroller.db["trades"][date][t]["sell-price"] = sell_p
		DB.masterDBcontroller.db["trades"][date][t]["fee"] = fee
		DB.masterDBcontroller.db["trades"][date][t]["profit"] = profit

		mongo = MongoClient('mongodb://anne:password@ds023550.mlab.com:23550/bitmon')
		db = mongo.bitmon
		transactions = db.transactions
		trx = {
			'date': date,
			'time': t,
			'sell_exchange': selling_e,
			'buy_exhange': buying_e,
			'buy_price': buy_p,
			'sell_price': sell_p,
			'fee': fee,
			'profit': profit
		}
		send = transactions.insert_one(trx)



	# Returns profit ratio from best spread between any 2 markets
	def __get_spread_info(self):
		lasts = []
		
		#### THIS NEEDS TO BE FIXED ####
		# # GET ALL LAST INFO FROM EACH EXCHANGE
		# lasts.append(DB.masterDBcontroller.getLast('COIN-BS'))
		# lasts.append(DB.masterDBcontroller.getLast("KRK"))

		# # Just get the last date
		# date = DB.masterDBcontroller.getLast('KRK')[2]

		# ex_buy = ''
		# ex_sell = ''
		# ex_pair = ''
		# my_buy = lasts[0][0]
		# my_sell = lasts[0][0]
		# for last_val in lasts:
		# 	if last_val[0] <= my_buy:
		# 		my_buy = last_val[0]
		# 		ex_buy = last_val[3]
		# 	if last_val[0] >= my_sell:
		# 		my_sell = last_val[0]
		# 		ex_sell = last_val[3]

		CB = float(get_data('COIN-BS')[2])
		KRK = float(get_data('KRK')[2])
		ITBT = float(get_data('ITBT')[2])
		print('-------------------------------------------------------------------------------------------------------------\n')
		print('LAST:  CB: ',CB,'  KRK: ',KRK, '  ITBT: ',ITBT)
		lasts.append(CB)
		lasts.append(KRK)
		lasts.append(ITBT)
		# fees pre-check
		CB_f = Decimal(CB*.01).quantize(Decimal('.01'), rounding=ROUND_UP) 
		KRK_f = Decimal(KRK*.0016).quantize(Decimal('.01'), rounding=ROUND_UP)
		ITBT_f = Decimal(ITBT*.002).quantize(Decimal('.01'), rounding=ROUND_UP)
		print('FEE:  CB: ', (CB_f),'  KRK: ',(KRK_f),'  ITBT: ',(ITBT_f), '\n')
		
		####################### THIS ALL CAN BE IMPROVED ###########################################################
		############################################################################################################

		loop = True

		# Used to repick selling and buying exchange if fees fuck shit up
		while(loop):

			loop = False
			my_sell = Decimal(max(lasts))
			my_buy = Decimal(min(lasts))	

			if my_sell == CB:
				ex_sell = 'COIN-BS'
				my_sell = Decimal(CB).quantize(Decimal('.01'), rounding=ROUND_UP) 
				fee_sell = CB_f
			elif my_sell == KRK:
				ex_sell = 'KRK'
				my_sell = Decimal(KRK).quantize(Decimal('.01'), rounding=ROUND_UP)
				fee_sell = KRK_f
			elif my_sell == ITBT:
				ex_sell = 'ITBT'
				my_sell = Decimal(ITBT).quantize(Decimal('.01'), rounding=ROUND_UP)
				fee_sell = ITBT_f
			if my_buy == CB:
				ex_buy = 'COIN-BS'
				my_buy = Decimal(CB).quantize(Decimal('.01'), rounding=ROUND_UP) 
				fee_buy = CB_f
			elif my_buy == KRK:
				ex_buy = 'KRK'
				my_buy = Decimal(KRK).quantize(Decimal('.01'), rounding=ROUND_UP)
				fee_buy = KRK_f
			elif my_buy == ITBT:
				ex_buy = 'ITBT'
				my_buy = Decimal(ITBT).quantize(Decimal('.01'), rounding=ROUND_UP)
				fee_buy = ITBT_f

			fee_total = fee_sell + fee_buy
			
			print('\nPROSPECT_BUYER: ', ex_sell, ' at ', my_buy, '  PROSPECT_SELLER: ', ex_buy , ' at ', my_sell, ' with ', fee_total, 'total fees')

			#Check Fee for Coinbase
			if ((my_sell - my_buy - fee_total) < self.baseline) and  (CB == my_buy or CB == my_sell):
				
				print(' \n --- Trade Not Profitable -- removing fee-heavy exchanges (Coin Base) ---')
				loop = True
				# ASSIUMING COIN BASE RIGHT NOW, fix later..  
				lasts.remove(CB)

		# REPLACE THIS HORRIBLE CODE SOON AND create the pair from ex_buy and ex_sell in alphebetical order.. 
		if (ex_buy == 'COIN-BS' or ex_buy == 'KRK') and (ex_sell == 'COIN-BS' or ex_sell == 'KRK'):
			ex_pair = 'COIN-BS/KRK'
		if (ex_buy == 'ITBT' or ex_buy == 'KRK') and (ex_sell == 'ITBT' or ex_sell == 'KRK'):
			ex_pair = 'ITBT/KRK'
		if (ex_buy == 'COIN-BS' or ex_buy == 'ITBT') and (ex_sell == 'COIN-BS' or ex_sell == 'ITBT'):
			ex_pair = 'COIN-BS/ITBT'

		############################################################################################################
		############################################################################################################


		profit_r = ((my_sell - my_buy) / my_buy)
		
		#temp_best_spread = DB.masterDBcontroller.getBestSpread()
		# what is this for?
		# if(profit_r >= temp_best_spread):
		# 	DB.masterDBcontroller.setBestSpread(profit_r, date)
		res = (float(my_buy), float(my_sell), float(profit_r), ex_buy, ex_sell, ex_pair)
		print('\n',res,'\n')
		return res


	def trade_decision(self):
		
		input_spread = self.__get_spread_info()
		buyingMKT_price = input_spread[0]
		sellingMKT_price = input_spread[1]
		spread = (sellingMKT_price - buyingMKT_price)
		spread_r = input_spread[2]
		ex_buy = input_spread[3]
		ex_sell = input_spread[4]
		ex_pair = input_spread[5]

		total_assets = get_balance(exchange='ALL')
		self.usd_assets = total_assets[0] 
		self.bc_assets = total_assets[1] 
		worth_unit = ((buyingMKT_price + sellingMKT_price) / 2)
		self.bc_worth = (self.usd_assets / worth_unit) + self.bc_assets
		self.usd_worth = (self.bc_assets * worth_unit) + self.usd_assets
		self.bc_r = self.bc_assets/self.bc_worth
		self.usd_r = self.usd_assets/self.usd_worth

		buyer_b = get_balance(exchange=ex_buy)
		seller_b = get_balance(exchange=ex_sell)
		buyer_usd_b = buyer_b[0]
		buyer_bt_b = buyer_b[1]

		### THE BTC BALANCE AND USD BALANCE ARE SWITHCED, CHECK GET BALANCE AND ABOVE ASSIGNMENTS. 

		seller_usd_b = seller_b[0]
		seller_bt_b = seller_b[1]
		# OTHER EXCHANGE ASSET DATA
		self.ex_dic[ex_pair]['usd_balance_r'] = buyer_usd_b / seller_usd_b
		
		print('\nBuyer USD Balace: ', buyer_usd_b)
		print('Seller USD Balance: ', seller_usd_b)
		print('EXCHANGE PAIR -- ', ex_pair)
		print('SPREAD_R      -- ', spread_r)

		# OTHER EXCHANGE PAIRS

		##################   MANAGE UNBALANCED ACCOUNTS   ##########################


		usd_balance_r = self.ex_dic[ex_pair]['usd_balance_r']
		

		print('USD_BALANCE R -- ', usd_balance_r)
		print('BTC_BALANCE R --', self.bc_r, '\n')
		# BUYING EXCHANGE HAS MORE USD 
		if (usd_balance_r > 2.285):

			difference = buyer_usd_b - seller_usd_b
			amount_usd = difference / 2
			last_ex_buy = self.ex_dic[ex_pair]['last_trade']['buy']['buyer']
			last_ex_sell = self.ex_dic[ex_pair]['last_trade']['sell']['seller']
			last_buy_price = self.ex_dic[ex_pair]['last_trade']['buy']['price']
			last_sell_price = self.ex_dic[ex_pair]['last_trade']['sell']['price']
			# REVERSE TRADE TO EVEN OUT ACCOUTS, BITCH
			if ex_buy == last_ex_sell and ex_sell == last_ex_buy:
				print('Reverse Trade Started')
				# WARNING! THIS COULD MAKE HIGH VOLUME TRADES 
				amount = amount_usd/buyingMKT_price
				trade = self.__makeTrade(ex_buy, ex_sell, ex_pair, amount, buyingMKT_price, sellingMKT_price)
				print(trade)
				return Trade
			
			# BUYING MARKET HAS NOT CHANGED 
			# If exchange with more USD can buy BTC for below last trade buy price to even out accounts and make some moneyyy
			elif (last_sell_price != None) and (buyingMKT_price > last_sell_price):              
				amount = buyer_bt_b / 2
				sell = self.__makeSell(ex_buy, amount)
				print(sell)
				print('Buying Exchange Balance Evened')
				if sellingMKT_price < last_buy_price:
				 	amount = (seller_usd_b / 2) / sellingMKT_price
				 	buy = self.__makeBuy(ex_sell, amount)
				 	print(buy)
				 	print('Selling Exchange Balance Evened')
				 	return
				else:
					print('WARNING! Buying Exchange Balance UNEVEN!')
					return
			
			print('Uneven Balance for this exchange pair not managed')
			print('-------------------------------------------------------------------------------------------------------------\n')	 	
			return ( False, buyingMKT_price, sellingMKT_price)
		
		
		# SELLING EXCHANGE HAS MORE USD
		elif (usd_balance_r < .35):

			difference = seller_usd_b - buyer_usd_b
			amount_usd = difference / 2
			last_ex_buy = self.ex_dic[ex_pair]['last_trade']['buy']['buyer']
			last_ex_sell = self.ex_dic[ex_pair]['last_trade']['sell']['seller']
			last_buy_price = self.ex_dic[ex_pair]['last_trade']['buy']['price']
			last_sell_price = self.ex_dic[ex_pair]['last_trade']['sell']['price']
			if ex_buy == last_ex_sell and ex_sell == last_ex_buy:
				print('Reverse Trade Started')
				# WARNING! THIS COULD MAKE HIGH VOLUME TRADES 
				amount = amount_usd/buyingMKT_price
				trade = self.__makeTrade(ex_buy, ex_sell, ex_pair, amount, buyingMKT_price, sellingMKT_price)
				print(trade)
				return
			# SELLING MARKET HAS NOT CHANGED
			# If exchange with more USD can buy BTC for below last trade buy price to even out accounts and make some moneyyy
			elif (last_buy_price != None) and (sellingMKT_price < last_buy_price):
				amount = (seller_usd_b / 2) / sellingMKT_price
				buy = self.__makeBuy(ex_sell, amount) 					# NOW SELLING EXCHANGE IS EVENED OUT
				print('Selling Exchange Balance Evened')
				#Check if buying exchange can be evened to fully even out pair of exchanges 
				if buyingMKT_price > last_sell_price:
					amount = buyer_bt_b / 2
					sell = self.__makeSell(ex_buy, amount)
					print(sell)
					print('Buying Exchange Balance Evened')
					return
				else:
					print('WARNING! Buying Exchange Balance UNEVEN!')
					return
			
			print('Uneven Balance for this exchange pair not managed ')
			print('-------------------------------------------------------------------------------------------------------------\n')		
			return ( False, buyingMKT_price, sellingMKT_price)


		
		####################################################################
		################        REGULAR PROCEDURE        ###################
		
		# we have more bitcoin than we should and spread looks GREAT. 
		if(self.bc_r > .4 and self.usd_assets > self.usd_base and spread_r > .021):
			volume = .400000
			amount_usd = buyer_usd_b * volume
			amount = amount_usd/buyingMKT_price
			trade = self.__makeTrade(ex_buy, ex_sell, ex_pair, amount, buyingMKT_price, sellingMKT_price)
			print('TRADE: ', trade)
			print('-------------------------------------------------------------------------------------------------------------\n')	
			return trade

		if(self.bc_r > .4 and self.usd_assets > self.usd_base and spread_r > .0185):
			volume = .400000
			amount_usd = buyer_usd_b * volume
			amount = amount_usd/buyingMKT_price
			trade = self.__makeTrade(ex_buy, ex_sell, ex_pair, amount, buyingMKT_price, sellingMKT_price)
			print('TRADE: ', trade)
			print('-------------------------------------------------------------------------------------------------------------\n')	
			return trade
			  

		# probably some logic in here to determine how much we wanna buy
		if(self.bc_r > .25 and self.usd_assets > self.usd_base and spread_r > 0.011):
			volume = .350000
			amount_usd = buyer_usd_b * float(volume)
			amount = amount_usd/buyingMKT_price
			trade = self.__makeTrade(ex_buy, ex_sell, ex_pair, amount, buyingMKT_price, sellingMKT_price)
			print('TRADE: ', trade)
			print('-------------------------------------------------------------------------------------------------------------\n')	
			return trade
		
		# Same ol shit
		if(self.bc_r > .10 and self.usd_assets > self.usd_base and spread_r >= 0.009):
			volume = .250000
			amount_usd = buyer_usd_b * float(volume)
			amount = amount_usd/buyingMKT_price

			if amount < .01:
				print('ABORTING TRADE, TRADE LESS THAN .01 BTC. Increase balance to resolve.')
				return
			
			trade = self.__makeTrade(ex_buy, ex_sell, ex_pair, amount, buyingMKT_price, sellingMKT_price)
			print('TRADE: ', trade)
			print('-------------------------------------------------------------------------------------------------------------\n')	
			return trade

		print('NO TRADE MADE -- Trade critera not met')
		print('\n-------------------------------------------------------------------------------------------------------------\n')
		return ( False, buyingMKT_price, sellingMKT_price)	



		#####################################################################

	
	def __makeTrade(self, buyer, seller, ex_pair, amount, buying_price, selling_price):

		######################################################################################################################
		####  REDUNDANT, I MOVED THIS FEE CHECK TO get_spread_info(), REMOVE once fee check in get_spread_info is dynamic ####
		######################################################################################################################
		#CHECK FEES AGAINST profit
		# coinbase has a buy / sell fee of 1%
		spread = selling_price - buying_price	

		if buyer == 'COIN-BS':
			fee = Decimal((.01)*(buying_price)*(amount))
			buy_fee = fee.quantize(Decimal('.01'), rounding=ROUND_UP)
		# kraken changes fee based on volume of trades per user. Will always be between 0.16% and 0.26%
		if buyer == 'KRK':
			fee = Decimal((.0016)*(buying_price)*(amount))								### ROUND THIS SHIT UP ###
			buy_fee = fee.quantize(Decimal('.01'), rounding=ROUND_UP)
		if buyer == 'ITBT':
			fee = Decimal((.002)*(buying_price)*(amount))			
			buy_fee = fee.quantize(Decimal('.01'), rounding=ROUND_UP)
		if seller == 'COIN-BS':
			fee = Decimal((.01)*(selling_price)*(amount))
			sell_fee = fee.quantize(Decimal('.01'), rounding=ROUND_UP)
		if seller == 'KRK':
			fee = Decimal((.0016)*(selling_price)*(amount))
			sell_fee = fee.quantize(Decimal('.01'), rounding=ROUND_UP)
		if seller == 'ITBT':
			fee = Decimal((.002)*(selling_price)*(amount))
			sell_fee = sell_fee = fee.quantize(Decimal('.01'), rounding=ROUND_UP)

		total_fee = buy_fee + sell_fee
		total_fee = float(total_fee)

		# Never make a trade that profits less than 25 cents
		if (spread - total_fee) < self.baseline:
			print('\n - - -  PROFIT LESS THAN BASELINE  - - -  \n - - -  TRADE ABORTED  - - - \n\n')
			return 
		##############################################################################################################
		##############################################################################################################


		# Make a trade and get rich
		else:

			self.__logTrade(buyer, seller, buying_price, selling_price, total_fee)


			self.ex_dic[ex_pair]['last_trade']['buy']['buyer'] = buyer
			self.ex_dic[ex_pair]['last_trade']['buy']['price'] = buying_price
			self.ex_dic[ex_pair]['last_trade']['sell']['seller'] = seller
			self.ex_dic[ex_pair]['last_trade']['sell']['price'] = selling_price

			buy(buyer, amount, buying_price ,'BTC')
			sell(seller, amount, selling_price ,'BTC')
			return ( True, (((selling_price - buying_price) * amount) - total_fee), buyer, seller, buying_price, selling_price, total_fee, sell)
			# MAY WANT TO QUERY ACTUAL DATA FROM BUY AND SELL to get final profit.


