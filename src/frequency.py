import xml.etree.ElementTree as ET
import csv
import sys
from collections import defaultdict
from Parser import *
import operator
from preprocess import *
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy
from numpy import *
from heapq import *
import re

def getQuerySkuDict(filename):
    inputFile = open(filename)
    reader = csv.reader(inputFile)
    querySkuDict = defaultdict(lambda: defaultdict(int))
    queryStat = defaultdict(int)
    par = Parser()
    for row in reader:
    	query = row[3]
    	query = preprocessQuery(query, par)
    	sku = row[1]
        queryStat[query] += 1
    	querySkuDict[query][sku] += 1
    return querySkuDict, queryStat

def getProductInfo():
    productTree = ET.parse('../data/small_product_data.xml')
    root = productTree.getroot()
    productSkus = []
    productDescpt = []
    for product in root.findall('product'):
        sku = product.find('sku').text
        description = product.find('longDescription').text
        productSkus.append(sku)
        productDescpt.append(description)
    return productSkus, productDescpt

def getDatumInfo(testFileName):    
    testFile = open(testFileName, 'r')
    reader = csv.reader(testFile)
    datum = []
    queries = []
    for row in reader:
        datum.append(row)
        queries.append(row[3])
    return datum, queries

def getQueryStats():
    trainFileName = '../data/psudo_train2.csv'
    querySkuDict, queryStat = getQuerySkuDict(trainFileName)
    sortedQuery = sorted(queryStat.items(), key=operator.itemgetter(1), reverse=True)
    top100 = sortedQuery[0:100]
    output = open('../data/result/top100query.txt','w')
    for queryDict in top100:
        query = queryDict[0]
        query = re.sub("\s","-",query)
        count = queryDict[1]
        query += " "
        outputStr = query * int(count*1.0 / 10)
        output.write(outputStr)
    output.close()




if __name__ == "__main__":
    trainFileName = '../data/psudo_train2.csv'
    testFileName = '../data/psudo_test2.csv'
    querySkuDict, queryStat = getQuerySkuDict(trainFileName)

    productSkus, productDescpt = getProductInfo()
    datum, queries = getDatumInfo(testFileName)
    corpus = []
    corpus.extend(productDescpt)
    corpus.extend(queries)

    vectorizer = TfidfVectorizer(min_df=1)
    tfidf = vectorizer.fit_transform(corpus)
    tfidfArray = tfidf.toarray()
    numProducts = len(productSkus)
    numQuery = len(datum)
    """
    for each query, I get the top five sku with product(tfidf(product), tfidf(query))
    """
    contentOutput = open('../data/result/content.csv','w')
    collabOutput = open('../data/result/frequency.csv','w')
    writer1 = csv.writer(contentOutput)
    writer2 = csv.writer(collabOutput)
    total = 0.0
    correct = 0.0
    correct1 = 0.0
    tmp = 0.0
    tmp1 = 0.0
    for x in range(0, numQuery):
        total += 1
        trueSku = datum[x][1]
        query = queries[x]
        #first do content-based filtering
        queryArray = tfidfArray[x+numProducts,:]
        scoreDict = {}
        for j in range(0, numProducts):
            prodArray = tfidfArray[j,:]
            score = numpy.dot(queryArray, prodArray)
            if score > 0:
                scoreDict[productSkus[j]] = score
        skusItems = nlargest(5, scoreDict.items(), key=operator.itemgetter(1))
        skus1 = []
        for sku in skusItems:
            skus1.append(sku[0])
        #then do collaborative filtering
        skus2 = []
        if query in querySkuDict:
            for sku in sorted( querySkuDict[query], key=querySkuDict[query].get, reverse = True ):
                skus2.append(sku)
            skus2 = skus2[0:5]
        writer1.writerow(skus1)
        writer2.writerow(skus2)
        if trueSku in skus1:
            correct1 += 1.0 / (skus1.index(trueSku) + 1)
            tmp1 += 1
        if trueSku in skus2:
            correct += 1.0 / (skus2.index(trueSku) + 1)
            tmp += 1

    print "frequence precision " + str(tmp/total)
    print "frequence score:     " + str(correct / total)




