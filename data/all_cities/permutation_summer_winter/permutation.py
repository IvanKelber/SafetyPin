import random
import argparse
import csv
import numpy

def load_file(file_path):
    data = []
    with open(file_path, 'r') as file_reader:
        row = file_reader.readline()
        data = [float(x) for x in row.split(',')]

    return data



def permutation_test():

	parser = argparse.ArgumentParser()
	parser.add_argument('-summer', required=True, help='Path to regular data')
	parser.add_argument('-winter', required=True, help='Path to holiday data')
	parser.add_argument('-iters', type=int, default=100000, help='Number of iterations to run')
	opts = parser.parse_args()

	summerCrime = load_file(opts.summer)
	winterCrime = load_file(opts.winter)
	iters = opts.iters
	
	mean_summer = numpy.mean(summerCrime)
	mean_winter = numpy.mean(winterCrime)
	print mean_summer
	print mean_winter
	nn,kk = len(summerCrime),0

	difference = mean_summer - mean_winter
	comb = numpy.concatenate([summerCrime,winterCrime])

	for i in range(opts.iters):
		numpy.random.shuffle(comb)
		kk += difference < numpy.abs(numpy.mean(comb[:nn]) - numpy.mean(comb[nn:]))
	print kk/float((opts.iters))


	# TODO: Fill in 


if __name__ == '__main__':
	permutation_test()
