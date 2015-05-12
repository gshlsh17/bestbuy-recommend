import xml.etree.ElementTree as ET
import csv
import sys
from collections import defaultdict
from Parser import *
import operator
import re
from dtw import dtw

def customDist(x, y):
	if x == y:
		return 0
	return 1

def spellChecker(sorted_query):
	spellDict = defaultdict(str)
	numDict = defaultdict(str)
	for i in xrange(len(sorted_query)-1, -1, -1):
		cur_dict = sorted_query[i]
		if len(cur_dict[0]) <= 4:
			continue
		for j in xrange(0, i):
			com_dict = sorted_query[j]
			if (len(cur_dict[0]) == len(com_dict[0])) and (com_dict[1] >= 10 * cur_dict[1]):
				dist, cost, path = dtw(list(cur_dict[0]), list(com_dict[0]), customDist)
				if cost[len(cur_dict[0]) - 1][len(com_dict[0]) - 1] <= 1 :
					if (not cur_dict[0] in spellDict) or (com_dict[1] > numDict[cur_dict[0]]):
						spellDict[cur_dict[0]] = com_dict[0]
						numDict[cur_dict[0]] = com_dict[1]
					#print cur_dict[0] + ' ==> ' + com_dict[0] + '  #: ' + str(cur_dict[1]) + ' ==> ' + str(com_dict[1])
			if (abs(len(cur_dict[0]) - len(com_dict[0])) == 1) and (com_dict[1] >= 10 * cur_dict[1]):
				dist, cost, path = dtw(list(cur_dict[0]), list(com_dict[0]), customDist)
				if cost[len(cur_dict[0]) - 1][len(com_dict[0]) - 1] <= 2 :
					if (not cur_dict[0] in spellDict) or (com_dict[1] > numDict[cur_dict[0]]):
						spellDict[cur_dict[0]] = com_dict[0]
						numDict[cur_dict[0]] = com_dict[1]
					#print cur_dict[0] + ' ==> ' + com_dict[0] + '  #: ' + str(cur_dict[1]) + ' ==> ' + str(com_dict[1])
	for word in spellDict:
		correctWord = spellDict[word]
		while correctWord in spellDict:
			correctWord = spellDict[correctWord]
		spellDict[word] = correctWord
	return spellDict

def preprocessQuery(query, par):
	queryList = par.tokenise(query)
	# here, we need to seperate number and charater in a single string
	queryList.sort()
	query = queryList[0]
	for i in xrange(1,len(queryList)):
		query += ' ' + queryList[i]
	return query

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

def getQueryFrequency(filename):
    inputFile = open(filename)
    reader = csv.reader(inputFile)
    queryFreq = defaultdict(int)
    par = Parser()
    for row in reader:
    	query = row[3]
    	queries = par.tokenise(query)
    	for query in queries:
    		queryFreq[query] += 1
    return queryFreq	

#if __name__ == "__main__":
trainFileName = 'data/psudo-train.csv'
testFileName = 'data/psudo-test.csv'
querySkuDict = getQuerySkuDict(trainFileName)
# if we handle with typos
# queryFreq = getQueryFrequency(trainFileName)
# sorted_query = sorted(queryFreq.items(), key=operator.itemgetter(1), reverse=True)
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







