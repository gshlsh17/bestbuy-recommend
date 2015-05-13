import xml.etree.ElementTree as ET
import csv
import sys
from collections import defaultdict
from Parser import *
import operator
from preprocess import *

def getQuerySkuDict(filename):
    inputFile = open(filename)
    reader = csv.reader(inputFile)
    querySkuDict = defaultdict(lambda: defaultdict(int))
    par = Parser()
    for row in reader:
    	query = row[3]
    	query = preprocessQuery(query, par)
    	sku = row[1]
    	querySkuDict[query][sku] += 1
    return querySkuDict	

#if __name__ == "__main__":
# trainFileName = '../data/psudo-train.csv'
# testFileName = '../data/psudo-test.csv'
# querySkuDict = getQuerySkuDict(trainFileName)
# if we handle with typos
queryFreq = getQueryFrequency()
sortedQuery = sorted(queryFreq.items(), key=operator.itemgetter(1), reverse=True)
spellDict = spellChecker(sortedQuery)
sortedDict = sorted(spellDict.items(), key=operator.itemgetter(0))

testFile = open(testFileName, 'r')
reader = csv.reader(testFile)
par = Parser()
total = 0
correct = 0

for row in reader:
	skus = []
	query = row[3] #need to modifed for true test file
	query = preprocessQuery(query, par) # get a new string, stemmed, ordered
	total += 1
	if query in querySkuDict:
		for sku in sorted( querySkuDict[query], key=querySkuDict[query].get, reverse = True ):
			skus.append(sku)
		skus = skus[0:5]
		if row[1] in skus:
			print 'Yes'
			correct += 1
		else:
			print 'No'







