# bit-mon
A Young Robot Grindin day and night on Bitcoin markets to bring home some Grease
--------------------------------------------------------------------------------

A bitcoin trading bot that exploits large spreads between bitcoin exchange market prices.

*Daylog.py* is no longer directly in use for the trading platform. It is being reconstructed for data analysis 
and predictive modeling purposes. Daylog essentially constructs “Snapshots” of data and filters to custom JSON DB.
Daylog also adjusts its call rate to all restful APIs dynamically based on the current performance.  


*trader.py* is the beef of the trading bot. Right now it is still synced with the custom DB. Currently in the process 
unattaching the two entities for faster performance.

REST API calls were built into personalized wrappers and aggregated into a file which both trader and daylog can call.This file is obviously ignored on git.   

-------------------------------------------------------------------------------

*dependencies:* krakenex, itbit_api, coinbase_client, requests.
