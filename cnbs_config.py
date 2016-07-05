#!/usr/bin/python3

import hashlib
import binascii
import os
from bitmon.db_controller import *

def load():
	if __name__ == "__main__":
	    #key = hash_up()[0]
		#secret = hash_up[1]
		# print('-- PICK EXCHANGE TO TEST --\n')
		# print('-- COIN-BS - COINBASE ------')
		# print('-- BLK-CHN - BLOCK CHAIN ----')
		# print('--   OKC   - OK COIN --------')
		# print('--   KRK   - Kraken  --------\n')

		# execute = input('Enter exchange to Test: ')
		initialize("COIN-BS")
		print("COIN-BS INITIALIZED")
		os.system('python3 tests/COIN-BS_test.py ')
