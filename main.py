import xml.etree.ElementTree as ET
import csv
import sys
from collections import defaultdict
from Parser import *
import operator


def preprocessQuery(query, par):
	queryList = par.tokenise(query)
	queryList.sort()
	query = queryList[0]
	for i in xrange(1,len(queryList)):
		query += ' ' + queryList[i]
	return query


def getQuerySkuDict(filename):
    inputFile = open(filename)
    reader = csv.reader(inputFile)
    reader.next() # drop header line
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
    reader.next() # drop header line
    queryFreq = defaultdict(int)
    par = Parser()
    for row in reader:
    	query = row[3]
    	queries = par.tokenise(query)
    	for query in queries:
    		queryFreq[query] += 1
    return queryFreq	

#if __name__ == "__main__":
trainFileName = 'data/train.csv'
querySkuDict = getQuerySkuDict(trainFileName)
queryFreq = getQueryFrequency(trainFileName)
sorted_query = sorted(queryFreq.items(), key=operator.itemgetter(1), reverse=True)



