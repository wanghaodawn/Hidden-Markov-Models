import math
from math import *
import sys
from sys import argv

# Global Variables
global list_prior, list_trans, list_emit
list_prior = []
list_trans = []
list_emit = []


# Main Function
def main():
	# Declare global variables

	# argvs are: python filename, dev, hmm-trans, hmm-emit, hmm-prior
	if len(sys.argv) != 5:
		print("ERROR: Incorrect arguments!")
		exit(-1)

	# Read hmm files
	read_prior(argv[4])
	read_trans(argv[2])
	read_emit(argv[3])

	# compute and output
	compute(argv[1])


# Compute and output
def compute(filename):
	# Declare global variables
	global list_prior, list_trans, list_emit

	f = open(filename, 'r')

	while 1:
		line = str(f.readline()).strip()
		if not line:
			break

		words = line.split(" ")
		i = 0
		prev_list = []
		curr_list = []

		# Traverse the words in each line
		for word in words:
			# Update the first word
			if i == 0:
				# Traverse each row in the table of current line
				for k in range(0, 8):
					temp = list_prior[k] + list_emit[k][word]
					prev_list.append(temp)
				i += 1
				continue

			# Traverse each row in the table of current line
			for k in range(0, 8):
				# Traverse each row in the table of prev_line and sum the result
				for j in range(0, 8):
					# print("prev_list: " + str(len(prev_list)))
					# print("list_trans: " + str(len(list_trans[j])))
					# print("j: " + str(j))
					# print("word: " + word)
					temp_temp = prev_list[j] + list_trans[j][k]
					if j == 0:
						temp = temp_temp
					else:
						temp = log_sum(temp, temp_temp)
				temp += list_emit[k][word]
				curr_list.append(temp)

			i += 1
			prev_list = curr_list
			# Keep the curr_list for last word
			if i != len(words):
				curr_list = []

		res = 0.0
		for j in range(0, 8):
			if j == 0:
				res = curr_list[j]
			else:
				res = log_sum(res, curr_list[j])
		print(res)


# Read trans file
def read_trans(filename):
	# Declare global variables
	global list_trans

	f = open(filename, 'r')

	while 1:
		line = str(f.readline()).strip()
		if not line:
			break

		lines = line.split(" ")
		if len(lines) != 9:
			continue

		temp_list = []

		for s in lines:
			ss = s.split(":")

			if len(ss) != 2:
				continue

			val_trans = -1.0
			try:
				val_trans = float(ss[1])
				# print("val: " + str(val))
			except ValueError:
				val_trans = -1.0
			if val_trans == -1.0:
				print("ERROR: Wrong number for val_trans!")
				exit(-1)

			temp_list.append(math.log(val_trans))

		list_trans.append(temp_list)

	# print("read_trans OUTPUT")
	# print(list_trans)


# Read emit file
def read_emit(filename):
	# Declare global variables
	global list_emit

	f = open(filename, 'r')

	while 1:
		line = str(f.readline()).strip()
		if not line:
			break

		lines = line.split(" ")
		temp_dic = {}

		for s in lines:
			ss = s.split(":")

			if len(ss) != 2:
				continue

			val_emit = -1.0
			try:
				val_emit = float(ss[1])
				# print("val: " + str(val))
			except ValueError:
				val_emit = -1.0
			if val_emit == -1.0:
				print("ERROR: Wrong number for val_trans!")
				exit(-1)

			temp_dic[ss[0]] = math.log(val_emit)

		list_emit.append(temp_dic)

	# print("read_emit OUTPUT")
	# print(list_emit)


# Read prior file
def read_prior(filename):
	# Declare global variables
	global list_prior

	f = open(filename, 'r')

	while 1:
		line = str(f.readline()).strip()
		if not line:
			break

		lines = line.split(" ")
		if len(lines) != 2:
			continue

		val_prior = -1.0
		try:
			val_prior = float(lines[1])
			# print("val: " + str(val))
		except ValueError:
			val_prior = -1.0
		if val_prior == -1.0:
			print("ERROR: Wrong number for val_prior!")
			exit(-1)

		list_prior.append(math.log(val_prior))

	# print("read_prior OUTPUT")
	# for i in list_prior:
		# print(str(i) + "\t")


# Computes log sum of two exponentiated log numbers efficiently
def log_sum(left, right):
	if right < left:
		return left + log1p(exp(right - left))
	elif left < right:
		return right + log1p(exp(left - right));
	else:
		return left + log1p(1)


if __name__ == "__main__":
	main()