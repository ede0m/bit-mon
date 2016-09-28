# bit-mon
A Young Robot Grindin day and night on Bitcoin markets to bring home some Grease


A bitcoin trading bot that exploits large spreads between bitcoin exchange market prices.

Daylog.py is no longer directly in use for the trading platform. It is being reconstructed for data analysis 
and predictive modeling purposes. Daylog essentially constructs “Snapshots” of data and filters to custom JSON DB.

trader.py is the beef of the trading bot. Right now it is still synced with the custom DB. Currently in the process 
unattaching the two entities for faster performance.

dependencies: krakenex, itbit_api, coinbase_client, requests.
