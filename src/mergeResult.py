import csv


filenames = ['../data/result/collab.csv', '../data/result/predictionsSVC.csv', '../data/result/content.csv']
results = [[],[],[]]
for i in xrange(3):
	with open(filenames[i], 'r') as f:
		reader = csv.reader(f)
		for row in reader:
			results[i].append(row)

scores = [1.0, 0.7, 0.5, 0.4, 0.3]
finalResult = []

