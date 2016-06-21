import json
from pprint import pprint
#!/usr/bin/python3
from pprint import pprint
from api_call import api_call

class Trade(object):

	def __init__(self):
		self.trade_log = []
		self.num_trades = 0
		self.lim_order_max = 0
		self.lim_order_min = 0
	
	def get_logs(self):
		return self.trade_log
	
	def initiate_trade():
		##STATISTACL CONDITIONS 
		pass
		
	def cross_site_analysis(self, market1):
		api = api_call()
		api.read_key()
		data = api.get_data(market1)
		print(data)		 


	def profit_tracker():
		#listtransactions coinbase API
		pass		

	#transfter BTC to potentially higher priced selling markets 
	# prepare to buy BTC with USD from lower priced markets
	# sell BTC and constantly move small portin of profits back to USD on low priced markets 
	def even_funds():
		pass	
			

