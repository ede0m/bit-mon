import sys
import time
sys.path.append('bitmon/')
import trader
import smtplib
 
if __name__ == "__main__":
    
    make_us_some_fucking_money = trader.Trader()

    count = 0
    while True:

    	trade = make_us_some_fucking_money.trade_decision()
    	time.sleep(60)
    	if count == 0 or count == 60 or trade[0] == True:
    		server = smtplib.SMTP('smtp.gmail.com', 587)
    		server.starttls()
    		server.login("cubone.btcballer@gmail.com", "OGPokemon1995")
    		
    		if trade[0] == False:
    			msg = "\nNO TRADE MADE THIS HOUR:  \nBest Buying Price: " + str(trade[1]) + '\n Best Selling Price: ' + str(trade[2])
    			count = 1 
    		if trade[0] == True:
    			msg = '\rCUBONE TRADE MADE: \n ' + 'BUYER: ' + trade[2] +' '+ str(trade[4]) + '\n' + 'SELLER: '+ trade[3] +' '+ str(trade[5]) +'\n' + 'PROFIT: ' + str(trade[1]) 


    		server.sendmail("cubone.btcballer@gmail.com", "ede0m25@gmail.com", msg)
    		print('SENT ALERT')
    		server.quit()
    	count = count + 1

    sys.exit(0)
