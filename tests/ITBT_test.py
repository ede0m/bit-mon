#!/usr/bin/python3
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append('bitmon/')
from Daylog import Daylog



day1 = Daylog('ITBT')
day1.log_day()