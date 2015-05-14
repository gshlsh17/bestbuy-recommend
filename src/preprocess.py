import csv
from collections import defaultdict
from Parser import *
import re
from dtw import dtw
import operator

def customDist(x, y):
	if x == y:
		return 0
	return 1

def preprocessQuery(query, par):
	# split the query by [-_] and any space
	queryWords = re.split('[-_\s]', query)
	# here, we need to seperate number and charater in a single string
	# notice, we can not modify the list when we iterate it
	tmp = []
	for word in queryWords:
		m = re.search("^[\D][\S]+[\d]+", word)
		if not (m is None):
			m = re.search("\d", word)
			idx = m.start()
			tmp.append(word[0:idx])
			tmp.append(word[idx:len(word)])
		else:
			tmp.append(word)
	queryWords = tmp
	# stemming each word in the query
	queryList = []
	for word in queryWords:
		words = par.tokenise(word)
		for word in words:
			queryList.append(word)
	queryList.sort()
	query = queryList[0]
	for i in xrange(1,len(queryList)):
		query += ' ' + queryList[i]
	return query

def spellChecker(queryFreq):
	sortedQuery = sorted(queryFreq.items(), key=operator.itemgetter(1), reverse=True)
	spellDict = defaultdict(str)
	numDict = defaultdict(int)
	for i in xrange(len(sortedQuery)-1, -1, -1):
		cur_dict = sortedQuery[i]
		if len(cur_dict[0]) <= 4:
			continue
		for j in xrange(0, i):
			com_dict = sortedQuery[j]
			if (len(cur_dict[0]) == len(com_dict[0])) and (com_dict[1] >= 10 * cur_dict[1]):
				dist, cost, path = dtw(list(cur_dict[0]), list(com_dict[0]), customDist)
				if cost[len(cur_dict[0]) - 1][len(com_dict[0]) - 1] <= 1 :
					if (not cur_dict[0] in spellDict) or (com_dict[1] > numDict[cur_dict[0]]):
						spellDict[cur_dict[0]] = com_dict[0]
						numDict[cur_dict[0]] = com_dict[1]
					#print cur_dict[0] + ' ==> ' + com_dict[0] + '  #: ' + str(cur_dict[1]) + ' ==> ' + str(com_dict[1])
			if (len(com_dict[0]) > 4) and (abs(len(cur_dict[0]) - len(com_dict[0])) <= 2) and (com_dict[1] >= 10 * cur_dict[1]):
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


def getQueryFrequency():
	# read all quries from both training file and test file
	count = 0
	queryFreq = defaultdict(int)
	par = Parser()
	# first add query word from train data
	inputFile = open('../data/train.csv')
	reader = csv.reader(inputFile)
	for row in reader:
		query = row[3]
		queries = preprocessQuery(query, par).split(" ")
		for query in queries:
			queryFreq[query] += 1
	inputFile.close()
	# second add query word from test data
	inputFile = open('../data/test.csv')
	reader = csv.reader(inputFile)
	for row in reader:
		query = row[2]
		queries = preprocessQuery(query, par).split(" ")
		for query in queries:
			queryFreq[query] += 1
	inputFile.close()
	return queryFreq
