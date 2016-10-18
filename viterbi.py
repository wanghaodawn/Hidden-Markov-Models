# 
# This file finished the Viterbi Algorithm of Hidden Markov Models
# By Hao Wang - haow2
# 04/08/2016
# 

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

	name = ["PR", "VB", "RB", "NN", "PC", "JJ", "DT", "OT"]

	while 1:
		line = str(f.readline()).strip()
		if not line:
			break

		words = line.split(" ")
		i = 0
		# print(len(words))
		# prev_list = []
		curr_list = [[0.0 for col in range(8)] for row in range(len(words))]
		 # [[0.0] * 8] * len(words)
		path      = [[0 for col in range(8)] for row in range(len(words))]

		# print(len(curr_list))
		# print(len(curr_list[0]))

		# Traverse the words in each line
		for word in words:
			# Update the first word
			if i == 0:
				# for m in range(0, len(words)):
				# 	print(path[m])
				# Traverse each row in the table of current line
				for k in range(0, 8):
					temp = list_prior[k] + list_emit[k][word]
					curr_list[0][k] = temp
					# print(temp)
				# 	break
				# for m in range(0, 8):
				# 	print(curr_list[0][m])

				# for m in range(0, len(words)):
				# 	print(curr_list[m])

				i += 1
				continue

			# for m in range(0, len(words)):
			# 	print(path[m])

			# Traverse each row in the table of current line
			for k in range(0, 8):
				max_val = -10000000000.0
				assert_num = curr_list[0][0]
				
				# Traverse each row in the table of prev_line and sum the result
				for j in range(0, 8):
					# print("prev_list: " + str(len(prev_list)))
					# print("list_trans: " + str(len(list_trans[j])))
					# print("j: " + str(j))
					# print("word: " + word)
					# assert curr_list[i-1][0] == assert_num

					# print("i: " + str(i) + "\tj: " + str(j))
					# print("dp: " + str(curr_list[i-1][j]) + "\ttrans: " + str(list_trans[j][k]) + "\temit: " + str(list_emit[k][word]))
					temp_temp = curr_list[i-1][j] + list_trans[j][k] + list_emit[k][word]
					# print("k: " + str(k) + "\tj: " + str(j) + "\ttemp_temp: " + str(temp_temp))
					# print("max_val: " + str(max_val))
					if temp_temp > max_val:
						# assert curr_list[i-1][0] == assert_num
						# print("j: " + str(j))
						max_val = temp_temp
						# print(curr_list[0][0])
						# print(curr_list[1][0])
						curr_list[i][k] = max_val
						path[i][k] = j


						# assert i == 1
						# assert max_val == temp_temp
						# assert k == 0
						# assert curr_list[i-1][0] == assert_num

				# print("path: " + str(path[i][k]))
				# print("max_val: " + str(max_val))
				# print("i: " + str(i) + "\tk: " + str(k) + "\tmax_eval: " + str(max_val))

				# print("dp: " + str(curr_list[i][k]))
				
			i += 1
			# prev_list = curr_list
			# Keep the curr_list for last word
			# if i != len(words):
				# curr_list = []

			# if i == 2:
			# 	break

		# for i in range(0, len(words)):
		# 	print(path[i])
		# print("\t")
		# for i in range(0, len(words)):
		# 	print(curr_list[i])

		# Find the best way
		# print(curr_list)
		# print(path)
		max_val = -1000000000.0
		max_index = -1
		# Find the series of best state of the best one
		for i in range(0, 8):
			if curr_list[len(words)-1][i] > max_val:
				max_index = i
				max_val = curr_list[len(words)-1][i]
		# print(max_index)

		# for m in range(0, len(words)):
		# 	print(path[m])

		# Get the result
		i = len(words) - 1
		res = ""
		while i >= 0:
			# print(path[i][max_index])
			# print(best_path[i])
			res = words[i] + "_" + name[max_index] + " " + res
			max_index = path[i][max_index]
			i -= 1
		print(res[0: len(res)-1])

		# break

		# print(curr_list)

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