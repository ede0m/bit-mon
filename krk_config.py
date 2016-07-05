#!/usr/bin/python3

import hashlib
import binascii
import os

from sys import executable
from subprocess import Popen
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
		initialize("KRK")
		print("KRK INITIALIZED")
		# Popen([executable, 'python3 tests/KRK_test.py'], creationflags=CREATE_NEW_CONSOLE)
		# subprocess.call(['terminal', '-x', 'tests/KRK_test.py'])

		# os.system("terminal 'python3 tests/KRK_test.py'")
		os.system("/bin/sh python3 tests/KRK_test.py")
		# Popen([executable, 'python3 tests/KRK_test.py'], shell=True)


		# os.system('python3 tests/KRK_test.py ')
 
load()