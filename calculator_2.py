import sys

def name_dict(n):
	dic = {}
	for i in n:
		try:
			dic[i.split(':')[0]] = int(i.split(':')[1])
		except ValueError:
			print("Please input a number")
	return dic

def calulator(dic):
	dic_2 = {}
	ls_tax = [1500, 4500, 9000, 35000, 55000, 80000]
	ls_rate = [0.03, 0.1, 0.2, 0.25, 0.3, 0.35, 0.45]
	ls_deduct = [0, 105, 555, 1005, 2755, 5505, 13505]
	for key, value in dic.items():
		n = 0
		if (value - 3500 - value * 0.165) < 0:
			salary = value * (1 - 0.165)
		elif (value - 3500 - value * 0.165) > 80000:
			tax = (value - 3500 - value * 0.165) * ls_rate[6] - ls_deduct[6]
			salary = value * (1 - 0.165) - tax
		else:
			for i in ls_tax:
				if (value - 3500 - value * 0.165) <= i:
					tax = (value - 3500 - value * 0.165) * ls_rate[n] - ls_deduct[n]
					salary = value * (1 - 0.165) - tax
					break
				n += 1
		dic_2[key] = salary
	return dic_2

def print_f(dic):
	for key, value in dic.items():
		print(key, ':', format(value, '.2f'))


if __name__ == "__main__":
	names = sys.argv[1:]
	name_dic = name_dict(names)
	cal_dict = calulator(name_dic)
	print_f(cal_dict)