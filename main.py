import sys
sys.path.append('bitmon/')
import trader

if __name__ == "__main__":
    
    make_us_some_fucking_money = trader.Trader()

    while True:

    	make_us_some_fucking_money.trade_decision()
    	time.sleep(900)

    sys.exit(0)