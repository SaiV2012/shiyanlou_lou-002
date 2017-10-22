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

	def calculator_ss(self, dict_conf, ex_salary):
		ss_rate = 0
		for value in dict_conf.values():
			if value > 1:
				continue
			ss_rate = ss_rate + value
		if ex_salary > dict_conf['JiShuH']:
			ss = dict_conf['JiShuH'] * ss_rate
		elif ex_salary < dict_conf['JiShuL']:
			ss = dict_conf['JiShuL'] * ss_rate
		else:
			ss = ex_salary * ss_rate
		return ss

	def calculator_tax(self, dict_conf, ex_salary):
		temp = ex_salary - self.calculator_ss(dict_conf, ex_salary) - 3500
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

	def calculator_salary(self):
		salary = ex_salary - self.calculator_ss(dict_conf, ex_salary) - self.calculator_tax(dict_conf, ex_salary)
		return salary

	def print_f(self, file, ls):
		with open(file, "w") as csvfile:
			writer = csv.writer(csvfile)
			writer.writerows(ls)


if __name__ == '__main__':
	conf = Configure(configfile)
	userdata = UserData(userfile)
	ls_all = []
	for k, v in userdata.get_user().items():
		ls_temp = []
		ls_temp.append(k)
		ls_temp.append(v)
		ss = userdata.calculator_ss(conf.get_config(), v)
		tax = userdata.calculator_tax(conf.get_config(), v)
		ls_temp.append(format(ss, '.2f'))
		ls_temp.append(format(tax, '.2f'))
		ls_temp.append(format((v-ss-tax), '.2f'))
		ls_all.append(ls_temp)
	userdata.print_f(gongzifile, ls_all)
