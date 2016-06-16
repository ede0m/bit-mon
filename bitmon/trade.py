<<<<<<< HEAD
import json
from coinbase.wallet.client import Client
from pprint import pprint
#import Lab_stat


#COINBASE API INSTALL
CB_key = 'OjUd5UscHV2mADPs'
CB_secret = '9Aoo0zPWIK5C0vZ4qIsrosbzQAIOVROe' 
client = Client(CB_key, CB_secret)

user = client.get_current_user()
#user_as_json_string = json.dumps(user)
#pprint(user_as_json_string)

=======
#!/usr/bin/python3

import json
#from coinbase.wallet.client import Client
from pprint import pprint
from api_call import api_call
#import Lab_stat


>>>>>>> ad9bba9ff5abb4f1261fe839c2a6219baebba2c0
class Trade(object):

	def __init__(self):
		self.trade_log = []
		self.num_trades = 0
		self.lim_order_max = 0
		self.lim_order_min = 0
	
	def get_logs(self):
		return self.trade_log
	
	def initiate_trade():
<<<<<<< HEAD
		##STATISTACL CONDITIONS 
		
		
=======
		pass
		
	def cross_site_analysis(self, market1):
		api = api_call()
		api.read_key()
		data = api.get_data(market1)
		print(data)		 


	def profit_tracker():
		#listtransactions coinbase API
		pass		
>>>>>>> ad9bba9ff5abb4f1261fe839c2a6219baebba2c0
	#transfter BTC to potentially higher priced selling markets 
	# prepare to buy BTC with USD from lower priced markets
	# sell BTC and constantly move small portin of profits back to USD on low priced markets 
	def even_funds():
<<<<<<< HEAD
		pass							
=======
		pass				




trade = Trade()
data_test = trade.cross_site_analysis('COIN-BS')
print(data_test)			
>>>>>>> ad9bba9ff5abb4f1261fe839c2a6219baebba2c0
