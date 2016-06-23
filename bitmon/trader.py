psuedo


bc_balance = 0 # this is the current bitcoin balance accross the three markets?
usd_balance = 0 # this is the current us dollar balance accross the three markets?
bc_worth = 0 # our current net worth in terms of bitcoin
usd_worth = 0 # our current net worth in terms of us dollars

bc_base = 0 # baseline for bc
usd_base = 0 # baseline for us dollars

bc_r = bc_balance/bc_worth # percentage of our net worth that is liquid bitcoin
usd_r = usd_balance/usd_worth # percentage of our net worth that is liquid us dollars

spread = 0 # current spread

buy = "" # variable controlling if we buy
sell = "" # variable controlling if we sell
# a combination of buy and sell can determine if we trade (do both)


execute = {
	"S" : "", # sell shit
	"B" : "", # buy shit
	"SB" : "" # TRADE shit
}


## We are going to need getters and setters for the balances/ratios/worths/spread

######################################################################################
####### Begins the section where we determine if we are buying/selling ###############



## UP FOR DISCUSSION ---> This are more of examples then code

def arbitrage():
	buy = "" # variable controlling if we buy
	sell = "" # variable controlling if we sell
	if(bc_r > .4 and bc_balance >= bc_base and spread > .015):
		sell = "S"
		# probably some logic in here to determine how much we wanna sell

	if(usd_r > .4 and usd_balance >= usd_base and spread > .015):
		buy = "B"
		# probably some logic in here to determine how much we wanna buy
	return sell + buy


execute[arbitrage()]

