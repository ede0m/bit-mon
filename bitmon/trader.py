import os, sys, json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_call import *

bc_assets = 0 # this is the current bitcoin balance accross the three markets?
usd_assets = 0 # this is the current us dollar balance accross the three markets?
bc_worth = 1 # TOTAL ASSETS (BTC and USD across all markets) represented in BTC
usd_worth = 1 # # TOTAL ASSETS (BTC and USD across all markets) represented in USD

bc_base = 0 # baseline for bc
usd_base = 0 # baseline for us dollars

bc_r = bc_assets/bc_worth # percentage of our net worth that is liquid bitcoin
usd_r = usd_assets/usd_worth # percentage of our net worth that is liquid us dollars




# a combination of buy and sell can determine if we trade (do both)
initiateTrade = {
	"S" : "", # sell shit
	"B" : "", # buy shit
	"SB" : "" # TRADE shit
}


# Returns the best spead from any market
def get_best_spread():
	#CB data
	with open(CB_db.json) as data_file:
		data = json.load(data_file)



## UP FOR DISCUSSION ---> This are more of examples then code

## This is supposed to sort of form a "filter" or "funnel" that 
## our data falls down and determines risk vs. return kinda
def trade_decision(spread):
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
	send_funds('COIN-BS', 'KRK', .01, 'BTC')
	

makeTrade()

#initiateTrade[arbitrage()]

