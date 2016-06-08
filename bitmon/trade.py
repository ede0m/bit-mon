import json
from coinbase.wallet.client import Client
from pprint import pprint
#import Lab_stat


#COINBASE API INSTALL

client = Client(CB_key, CB_secret)

user = client.get_current_user()
#user_as_json_string = json.dumps(user)
#pprint(user_as_json_string)

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
		
	
	def cross_site_analysis(market1, market2):
		 
		pass

	def profit_tracker():
		#listtransactions coinbase API
		pass		
	#transfter BTC to potentially higher priced selling markets 
	# prepare to buy BTC with USD from lower priced markets
	# sell BTC and constantly move small portin of profits back to USD on low priced markets 
	def even_funds():
		pass							
