from itbit_api import itBitApiConnection
import requests

ITBT_user = 'D8951FD5-6ECB-497B-8634-448FFF00E30A'
ITBT_wallet_id = '94da7f29-05f4-4d62-9da8-0a51ef4e3601'
ITBT_key = 'WmBaMDA6ke5P5UC2YxJ6Zw'
ITBT_secret = 'tdHxdlO/QfJUu3+nt8pv+sOQFZ1sJhuztbHdw5Pgywg'



itbit_api_conn = itBitApiConnection(clientKey=ITBT_key, secret=ITBT_secret, userId=ITBT_user)
print(itbit_api_conn)
buy = itbit_api_conn.create_order(ITBT_wallet_id, 'buy', 'XBT', str(.001), str(620), 'XBTUSD' )
print(buy)
	