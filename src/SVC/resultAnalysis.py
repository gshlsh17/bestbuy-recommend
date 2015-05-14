import directory
import csv
import copy
import codecs
import sys



def analyze(test_file = directory.TESTING_DATA_FILE, result_file = directory.TESTING_PREDICTIONS_FILE, method = 0):
	score = 0.0
	map_score = 0.0
	real_skus = list()
	predict_skus = list()

	# read the real skus of the testing data
	with codecs.open(test_file, encoding='utf-8', mode='rb') as reader:
		for row in reader:
			_, sku, _, _, _, _ = row.split(',')
			real_skus.append(int(sku))

	


    # read the real skus of the testing data
	with open(result_file, 'r') as f:
		reader = csv.reader(f)
		for row in reader:
			predict_skus.append(row)
    		


	# print "len of real_skus: %d" %len(real_skus)
	# print "len of predict_skus: %d" %len(predict_skus)
	for i in range(len(real_skus)):
		for val in predict_skus[i]:
			if real_skus[i] == int(val):
				score += 1.0
				map_score += 1.0/(predict_skus[i].index(val) + 1)


	


	print "precision: %f" %(score/len(real_skus))
	print "score:     %f" %((map_score)/len(real_skus))




if __name__ == '__main__':
    analyze(sys.argv[1], sys.argv[2])
