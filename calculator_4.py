#!/usr/bin/env python3

from multiprocessing import Process, Queue
import sys
import csv
import os, time

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

	def get_user(self, q):
		with open(self.file) as file:
			for i in file.readlines():
				self.userdata[i.split(',')[0]] = int(i.split(',')[1].strip())
		return self.userdata
		q.put(self.userdata)

	def calculator_ss(self, dict_conf, ex_salary, q):
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
		q.put(ss)
		time.sleep(0.01)

	def calculator_tax(self, dict_conf, ex_salary, q):
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
		q.put(tax)
		time.sleep(0.01)

	def calculator_salary(self):
		salary = ex_salary - self.calculator_ss(dict_conf, ex_salary) - self.calculator_tax(dict_conf, ex_salary)
		return salary

	def print_f(self, file, ls):
		if os.path.isfile(file):
			with open(file, "a") as file:
				csv.writer(file).writerow(ls)
		else:
			with open(file, "w") as file:
				csv.writer(file).writerow(ls)
		time.sleep(0.01)

if __name__ == '__main__':
	q = Queue()
	conf = Configure(configfile)
	userdata = UserData(userfile)
	dict_conf = conf.get_config()
	v = 1
	p1 = Process(target=userdata.get_user, args=(q,))
	p1.start()
	for k, v in q.get().items():
		ls_temp = []
		ls_temp.append(k)
		ls_temp.append(v)
		p2 = Process(target=userdata.calculator_ss, args=(dict_conf, v, q))
		p3 = Process(target=userdata.calculator_tax, args=(dict_conf, v, q))
		p2.start()
		ss = q.get()
		#p2.join()
		p3.start()
		tax = q.get()
		#p3.join()
		ls_temp.append(format(ss, '.2f'))
		ls_temp.append(format(tax, '.2f'))
		ls_temp.append(format((v-ss-tax), '.2f'))
		p4 = Process(target=userdata.print_f, args=(gongzifile, ls_temp))
		p4.start()
		#p4.join()
	p1.join()
	p2.join()
	p3.join()
	p4.join()