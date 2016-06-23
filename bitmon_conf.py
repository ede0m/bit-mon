#!/usr/bin/python3

import hashlib
import binascii
import os
# import sys
# sys.path.append('/Users/Cormick/Downloads/bitmon 2/bit-mon/bitmon/')

# import db_controller

# db_controller.init()

#should set as environmental but w/e
#CB_key = 'OjUd5UscHV2mADPs'
#CB_secret = '9Aoo0zPWIK5C0vZ4qIsrosbzQAIOVROe'


def hash_up():
	CB_key = hashlib.pbkdf2_hmac('sha256', CB_Key, 'livestrong', 200)
	CB_secret = hashlib.pbkdf2_hmac('sha256', CB_secret, 'livestrong', 200)
	return (CB_key, CB_secret)

if __name__ == "__main__":
    #key = hash_up()[0]
	#secret = hash_up[1]
	print('-- PICK EXCHANGE TO TEST --\n')
	print('-- COIN-BS - COINBASE ------')
	print('-- BLK-CHN - BLOCK CHAIN ----\n')
	print('-- OKC --- - OK COIN bejing -\n')
	execute = input('Enter exchange to Test: ')
	os.system('python3 '+ execute + '_call.py ')
 

