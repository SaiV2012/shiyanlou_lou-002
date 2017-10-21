#!/usr/bin/env python3

import sys
import csv
import os

args = sys.argv[1:]
path = '/home/shiyanlou/'

try:
	index_c = args.index('-c')
	index_d = args.index('-d')
	index_o = args.index('-o')
except ValueError:
	print("Parameter Error")
	sys.exit()

configfile = args[index_c + 1]
userfile = args[index_d + 1]
gongzifile = args[index_o + 1]

if os.path.exists(configfile) and os.path.exists(userfile):
	pass
else:
	print("File Error")
	sys.exit()

if configfile[-3:] == 'cfg' and userfile[-3:] == 'csv':
	pass
else:
	print("File Type Error")
	sys.exit()

class Configure(object):
	def __init__(self, file):
		self.file = file
		self.config = {}

	def get_config(self):
		with open(self.file) as file:
			for i in file.readlines():
				self.config[i.split('=')[0].strip()] = float(i.split('=')[1].strip())
		return self.config

class UserData(object):
	def __init__(self, file):
		self.file = file
		self.userdata = {}

	def get_user(self):
		with open(self.file) as file:
			for i in file.readlines():
				self.userdata[i.split(',')[0]] = int(i.split(',')[1].strip())
		return self.userdata

	def calculator(self, ss):
		temp = value - ss - 3500
		if temp < 0:
			tax = 0
		elif temp < 1500:
			tax = temp * 0.03 - 0
		elif temp < 4500:
			tax = temp * 0.1 - 105
		elif temp < 9000:
			tax = temp * 0.2 - 555
		elif temp < 35000:
			tax = temp * 0.25 - 1005
		elif temp < 55000:
			tax = temp * 0.3 - 2755
		elif temp < 80000:
			tax = temp * 0.35 - 5505
		else:
			tax = temp * 0.045 - 13505
		return tax

conf = Configure(configfile)
userdata = UserData(userfile)

ss_rate = 0
for value in conf.get_config().values():
	if value > 1:
		continue
	ss_rate = ss_rate + value

ls_all = []
for key, value in userdata.get_user().items():
	ls_temp = []
	if value > conf.get_config()['JiShuH']:
		ss = conf.get_config()['JiShuH'] * ss_rate
	elif value < conf.get_config()['JiShuL']:
		ss = conf.get_config()['JiShuL'] * ss_rate
	else:
		ss = value * ss_rate
	tax = userdata.calculator(ss)
	salary = value - ss - tax
	ls_temp.append(key)
	ls_temp.append(value)
	ls_temp.append(format(ss, '.2f'))
	ls_temp.append(format(tax, '.2f'))
	ls_temp.append(format(salary, '.2f'))
	ls_all.append(ls_temp)

with open(gongzifile, "w") as csvfile:
	writer = csv.writer(csvfile)
	writer.writerows(ls_all)
