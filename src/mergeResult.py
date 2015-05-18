import csv
from collections import defaultdict
import operator

if __name__ == "__main__":
	filenames = ['../data/result/frequency.csv', '../data/result/predictionsSVC.csv', '../data/result/content.csv']
	results = [[],[],[]]
	for i in xrange(3):
		with open(filenames[i], 'r') as f:
			reader = csv.reader(f)
			for row in reader:
				results[i].append(row)

	scores = [1.0, 0.7, 0.5, 0.4, 0.3]
	weights = [1.0, 1.1, 0.1]
	finalResult = []
	for i in xrange(len(results[0])): # for every query
		skuScore = defaultdict(float)
		for j in xrange(3): # for every method
			skus = results[j][i] 
			for k in xrange(len(skus)): # for every single predict
				sku = skus[k]
				skuScore[sku] += scores[k] * weights[j] # since it's a defautdict, just add the score
		# sort the dict by its score, find the top 5 skus
		sortedSkus = sorted(skuScore.items(), key=operator.itemgetter(1), reverse=True)
		sortedSkus = sortedSkus[0:5]
		skus = []
		for x in xrange(5): # save the top5 result
			skus.append(sortedSkus[x][0])
		finalResult.append(skus)


	trueSkus = []
	with open('../data/psudo_test2.csv', 'r') as f:
		reader = csv.reader(f)
		for row in reader:
			trueSkus.append(row[1])

	# write to files
	# with open('../data/result/final-result.csv','w') as f:
	# 	writer = csv.writer(f)
	# 	for row in finalResult:
	# 		writer.writerow(row)

	total = 0.0
	score = 0.0
	tmp = 0.0
	for i in xrange(len(finalResult)):
		total += 1
		trueSku = trueSkus[i]
		predict = finalResult[i]
		if trueSku in predict:
			tmp += 1
			score += 1.0 / (predict.index(trueSku) + 1)

	print "precision: " + str(tmp/total)
	print "score:     " + str(score/total)

