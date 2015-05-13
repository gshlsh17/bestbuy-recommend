import csv
import random

'''
random split modified_train.csv into two parts. First parts called psudo_train2.csv, second part is psudo_test2.csv
'''

inputFile = open('../data/modified_train.csv')
reader = csv.reader(inputFile)
rows = []
for row in reader:
	rows.append(row)

idx = range(0, len(rows))
random.seed()
random.shuffle(idx) # idx is shuffled
partition = int(round(0.9 * len(rows)))
train_idx = idx[0:partition]
test_idx = idx[partition:len(rows)]
train_idx.sort()
test_idx.sort()

# output to psudo_train2.csv
with open('../data/psudo_train2.csv', 'w') as f:
	writer = csv.writer(f)
	for index in train_idx:
		writer.writerow([rows[index][0],rows[index][1],rows[index][2],rows[index][3],rows[index][4],rows[index][5]])

# output to psudo_test2.csv
with open('../data/psudo_test2.csv', 'w') as f:
	writer = csv.writer(f)
	for index in test_idx:
		writer.writerow([rows[index][0],rows[index][1],rows[index][2],rows[index][3],rows[index][4],rows[index][5]])