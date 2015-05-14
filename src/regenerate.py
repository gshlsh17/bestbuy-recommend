import csv
from preprocess import *
from Parser import *

"""
regenerate files with the pre-processed quries
each query is split by [_-\s]
seperate those number and words like 'nba2012', 'xbox360' into 'nba', '2012', 'xbox', '360'
then stemming each word, order each word and concat words into a new query
Also, have a spellChecker dict. key is the mis-spelled word, value is the true word. This is done by unsupervised learning
In this script, we reorder query and replace mis-spelled words. Then, write into file again
The query in new file is splited by space, stemmed, corrected, and reordered
"""

if __name__ == "__main__":
	queryFreq = getQueryFrequency()
	spellDict = spellChecker(queryFreq)
	regenerateFile('../data/train.csv', '../data/modified_train.csv', 3, spellDict)
	regenerateFile('../data/test.csv', '../data/modified_test.csv', 2, spellDict)

# regenerate 
def regenerateFile(inputName, outputName, idx, spellDict):
	par = Parser()
	inputFile = open(inputName)
	reader = csv.reader(inputFile)
	rows = []
	for row in reader:
		query = row[idx]
		query = preprocessQuery(query, par) # get the query that is stemmed, reordered but not corrected
		queries = query.split(" ")
		newQueries = []
		for word in queries:
			if word in spellDict:
				newQueries.append(spellDict[word])
			else:
				newQueries.append(word)
		newQueries.sort()
		query = newQueries[0]
		for i in xrange(1,len(newQueries)):
			query += " " + newQueries[i]
		row[idx] = query
		rows.append(row)
	# write each to a new file
	with open(outputName, 'w') as f:
		writer = csv.writer(f)
		for row in rows:
			if idx == 3:
				writer.writerow([row[0],row[1],row[2],row[3],row[4],row[5]])
			else:
				writer.writerow([row[0],row[1],row[2],row[3],row[4]])
